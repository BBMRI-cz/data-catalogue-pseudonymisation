import os
import pandas as pd
from pseudonymization.process.clinical_finder import ClinicalInfoFinder

from ..pseudonimization_api.pseudonimize_patient import PseudonymizePatient
from ..pseudonimization_api.pseudonimize_predictive import PseudonymizePredictive
from ..models.Patient import Patient
from ..models.Tissue import Tissue
from ..models.Genome import Genome
from ..models.Serum import Serum

import logging
import json
import subprocess

class RunPseudonimizer():

    def __init__(self, run_path, pseudo_tables_folder_path):
        self.patient_pseudo_table = os.path.join(pseudo_tables_folder_path, "patients.json")
        self.predictive_pseudo_table = os.path.join(pseudo_tables_folder_path, "predictive.json")
        self.sample_pseudo_table = os.path.join(pseudo_tables_folder_path, "samples.json")
        self.run_path = run_path

    def __call__(self):
        pred_pseudo_tuples = self._get_all_predictive_numbers_pseudonymize_sample_sheet()
        for pred, pseudo in pred_pseudo_tuples:
            self._pseudonymize_file_names_recursively(pred, pseudo, self.run_path)
            self._try_pseudonimize_content_of_files(pred, pseudo)
            clinical_data = ClinicalInfoFinder(self.run_path).collect_clinical_data(pred)

            if clinical_data:
                clinical_data_for_saving = self._prepare_clinical_data_for_saving(clinical_data, pseudo)
                self._save_clinical_data(clinical_data_for_saving,
                                        os.path.join(self.run_path, "catalog_info_per_pred_number"),
                                        pseudo)


    def _get_all_predictive_numbers_pseudonymize_sample_sheet(self):
        sample_sheet_path = os.path.join(self.run_path, "SampleSheet.csv")
        df = pd.read_csv(sample_sheet_path, delimiter=",",
                 names=["[Header]","Unnamed: 1","Unnamed: 2","Unnamed: 3","Unnamed: 4",
                 "Unnamed: 5","Unnamed: 6","Unnamed: 7","Unnamed: 8","Unnamed: 9"])
        
        sample_list_header = df["[Header]"].to_list()
        sample_list_second = df["Unnamed: 1"].to_list()
        id = sample_list_header.index("Sample_ID") +1

        predictive_numbers = sample_list_header[id:]
        predictive_pseudonimizer = PseudonymizePredictive(self.predictive_pseudo_table)
        pseudo_numbers = [predictive_pseudonimizer.pseudonimize(pred_number) for pred_number in predictive_numbers]

        new_column_header = sample_list_header[:id] + pseudo_numbers
        new_column_second = sample_list_second[:id] + pseudo_numbers

        df.drop(["[Header]", "Unnamed: 1"], axis=1, inplace=True)
        df.insert(loc=0, column="", value = new_column_second)
        df.insert(loc=0, column="[Header]",  value = new_column_header)
        df.columns = ["[Header]"] + ["" for i in range(len(df.columns) - 1)]
        df.fillna('', inplace=True)
        df.to_csv(sample_sheet_path, header=False, index=False)

        predictive_pseudo_tuples = [(predictive_numbers[i], pseudo_numbers[i]) for i in range(len(predictive_numbers))]

        return predictive_pseudo_tuples
    
    def _pseudonymize_file_names_recursively(self, text_to_replace, replaced_text, current_file):        
        current_file_renamed = current_file[::-1].replace(text_to_replace[::-1], replaced_text[::-1], 1)[::-1]
        os.rename(current_file, current_file_renamed)
        for file in os.listdir(current_file_renamed):
            file_path = os.path.join(current_file_renamed, file)
            if os.path.isdir(file_path):
                self._pseudonymize_file_names_recursively(text_to_replace, replaced_text, file_path)
            else:
                os.rename(
                    os.path.join(current_file_renamed, file), 
                    os.path.join(current_file_renamed, file.replace(text_to_replace, replaced_text))
                    )

    def _try_pseudonimize_content_of_files(self, pred_number, pseudo_pred_number):
        subprocess.call(["pseudonymization/replace_predictive.sh", self.run_path, pred_number, pseudo_pred_number])

    def _prepare_clinical_data_for_saving(self, patient_clinical_data, pseudo_id):
        samples = [self._prepare_sample(sample, pseudo_id) for sample in patient_clinical_data["samples"]]
        samples.sort()

        pseudo_patient_id = PseudonymizePatient(patient_clinical_data["ID"], self.patient_pseudo_table)()
        patient = Patient(
            pseudo_patient_id,
            patient_clinical_data["birth_date"],
            patient_clinical_data["sex"],
            samples
            )

        return patient


    def _prepare_sample(self, sample, pseudo_id):
        if sample["type"] == "Tissue":
            return Tissue(sample, pseudo_id, self.sample_pseudo_table)
        elif sample["type"] == "Genome":
            return Genome(sample, pseudo_id, self.sample_pseudo_table)
        elif sample["type"] == "Serum":
            return Serum(sample, pseudo_id, self.sample_pseudo_table)
        else:
            logging.error("Non existing sample tipe")
            return None
        

    def _save_clinical_data(self, patient: Patient, destination_path, pseudo_pred_number) -> dict:
        serialized_patient = patient.serialize()
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        with open(os.path.join(destination_path, f"{pseudo_pred_number}.json"), "w") as f:
            json.dump(serialized_patient, f, indent=4)
