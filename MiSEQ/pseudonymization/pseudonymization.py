import json
import os
import pandas as pd
import xml.etree.ElementTree as ET
import argparse
import uuid
from clinical_finder import FindClinicalInfo

class Pseudonymizer:
    """
    Pseudonymizer Class

    Attributes
    ----------
    run_path : str
        path to a sequencing run that will be pseudonymized and completed with clinical data
    export_path : str
        path to an file that consist of XML exports with biobank and clinical information
    pseudo_table_path :  str
        path to a pseudonymization json file

    Methods
    -------
    __call_(self)
        Performs the following steps:
            1. Pseudonymization of sample sheet
            2. Adding clinical and biobank data
            3. Pseudonymizing file names
    """

    xml_prefix = "{http://www.bbmri.cz/schemas/biobank/data}"

    def __init__(self, run_path, bbm_export_folder_path,
                 pseudonimisation_tables_path):
        """
        Parameters
        ----------
        run_path : str
            path to a sequencing run that will be pseudonymized and completed with clinical data
        export_path : str
            path to an file that consist of XML exports with biobank and clinical information
        pseudo_table_path :  str
            path to a pseudonymization json file
        """

        self.run_path = run_path
        self.export_path = bbm_export_folder_path
        self.pseudonimisation_tables_path = pseudonimisation_tables_path
        self.pseudo_pred_path = os.path.join(pseudonimisation_tables_path, "predictive.json")
        self.pseudo_patient_path = os.path.join(pseudonimisation_tables_path, "patient.json")
        self.pseudo_samples_path = os.path.join(pseudonimisation_tables_path, "samples.json")

    def __str__(self) -> str:
        return f"""Path to processed sequence run:\n {self.seq_path}\n
                Path to export folder:\n {self.export_path}\n
                Path to pseudonimisation_table: \n {self.pseudo_pred_path}"""

    def __call__(self):
        self.pseudonymize_run()

    def pseudonymize_run(self):
        """Performs the following steps:
        1. Pseudonymization of sample sheet
        2. Adding clinical and biobank data
        3. Pseudonymizing file names
        """

        predictive_pseudo_tuples = self._pseudo_sample_sheet_and_get_clinical_data()
        predictive_pseudo_tuples.sort(key=lambda a: len(a[0]), reverse=True)
        self._create_temporary_pseudo_table(predictive_pseudo_tuples)
        self._locate_all_files_with_predictive_number(predictive_pseudo_tuples)

    def _pseudo_sample_sheet_and_get_clinical_data(self):
        """Pseudonymizes run SampleSheet and 
        collect clinical data of predictive number in a given run

        Performs the following steps:
        1.Reads SampleSheet
        2.Pseudonymizes all predictive numbers
        3.Stores predictive:pseudo tuples to json
        4.Collects clinical data

        Returns
        -------
        clinical_data : List[Dict]
            List of dictionaries containing clinical information about a patient with a given predictive number
        predictive_pseudo_tuples : List[(str,str)]
            List of tuples (predictive_number:pseudonymized_number)
        """

        sample_sheet_path = os.path.join(self.run_path, "SampleSheet.csv")
        df = pd.read_csv(sample_sheet_path, delimiter=",",
                 names=["[Header]","Unnamed: 1","Unnamed: 2","Unnamed: 3","Unnamed: 4",
                 "Unnamed: 5","Unnamed: 6","Unnamed: 7","Unnamed: 8","Unnamed: 9"])
        
        sample_list_header = df["[Header]"].to_list()
        sample_list_second = df["Unnamed: 1"].to_list()
        id = sample_list_header.index("Sample_ID") +1


        predictive_numbers = sample_list_header[id:]
        predictive_numbers_original = predictive_numbers
        predictive_numbers = [predictive_number.replace("_", "-") for predictive_number in predictive_numbers]

        clinical_info_finder = FindClinicalInfo(self.export_path, predictive_numbers_original, self.pseudonimisation_tables_path, self.run_path)
        clinical_info_finder()
        pseudo_list = clinical_info_finder.get_pseudo_ids()

        new_column_header = sample_list_header[:id] + pseudo_list
        new_column_second = sample_list_second[:id] + pseudo_list

        df.drop(["[Header]", "Unnamed: 1"], axis=1, inplace=True)
        df.insert(loc=0, column="", value = new_column_second)
        df.insert(loc=0, column="[Header]",  value = new_column_header)
        df.columns = ["[Header]"] + ["" for i in range(len(df.columns) - 1)]
        df.fillna('', inplace=True)
        df.to_csv(sample_sheet_path, header=False, index=False)

        predictive_pseudo_tuples = [(predictive_numbers[i], pseudo_list[i]) for i in range(len(predictive_numbers))]

        return predictive_pseudo_tuples

    def _create_temporary_pseudo_table(self, predictive_pseudo_tuples):
        """Create a temporary pseudonymisation_table json file consisting
        only of predictive:pseudo tuples of a current run

        Parameters
        ----------
        predictive_pseudo_tuples : List[(str:str)]
            List of predictive:pseudo tuples
        """

        pseudo_list = [{"predictive_number": pred, "pseudo_number": pseudo} for pred, pseudo in predictive_pseudo_tuples] 
        data = {"pseudonimisation": pseudo_list}
        with open(f"{self.pseudo_pred_path}.temp", 'w+') as outfile:
            json.dump(data, outfile, indent=4)

    def _locate_all_files_with_predictive_number(self, predictive_pseudo_tuples):
        """Locate all files in a run that contain a predictive number in the name 
        and replace it with pseudonymized predictive number

        Parameters
        ----------
        predictive_pseudo_tuples : List[(str:str)]
            List of predictive:pseudo tuples
        """

        for pred, pseudo in predictive_pseudo_tuples:
            self._rename_files_recursively(pred, pseudo, self.run_path)

    def _rename_files_recursively(self, text_to_replace, replaced_text, current_file):
        """Recursively renames all files ina run that contain predictive number with
        pseudonymized predictive number. Does it in a way to not create conflicts in a renaming

        Parameters
        ----------
        text_to_replace : str
            Text that should be replaced in a file name
        replaced_text : str
            Text that will replace "text_to_replace" in a file name
        current_file : str
            Path of a current directory that will be renamed and then listed to rename inner file
        """
        
        current_file_renamed = current_file[::-1].replace(text_to_replace[::-1], replaced_text[::-1], 1)[::-1]
        os.rename(current_file, current_file_renamed)
        for file in os.listdir(current_file_renamed):
            file_path = os.path.join(current_file_renamed, file)
            if os.path.isdir(file_path):
                self._rename_files_recursively(text_to_replace, replaced_text, file_path)
            else:
                os.rename(os.path.join(current_file_renamed, file), os.path.join(current_file_renamed, file.replace(text_to_replace, replaced_text)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Pseudonymizer",
        description="Pseudonymize sequencing run and adds clinical data to it")
    parser.add_argument("-r", "--run", type=str, required=True, help="Path to sequencing run path that will be pseudonymized")
    parser.add_argument("-e", "--export", type=str, required=True, help="Path to Biobank Export to extract clinical data")
    parser.add_argument("-p", "--pseudo", type=str, required=True, help="Path to pseudonymization json files")
    args = parser.parse_args()
    
    Pseudonymizer(args.run, args.export, args.pseudo)()