import os
import pandas as pd

from .run_pseudonymizer import RunPseudonymizer
from pseudonymization.pseudonimization_api.pseudonimize_predictive import PseudonymizePredictive

class NextSeqPseudonymizer(RunPseudonymizer):

    def __init__(self, run_path, pseudo_tables_folder_path):
        self.patient_pseudo_table = os.path.join(pseudo_tables_folder_path, "patients.json")
        self.predictive_pseudo_table = os.path.join(pseudo_tables_folder_path, "predictive.json")
        self.sample_pseudo_table = os.path.join(pseudo_tables_folder_path, "samples.json")
        self.run_path = run_path

    def pseudonymize(self):
        pred_pseudo_tuples = self._get_all_predictive_numbers_pseudonymize_sample_sheet()
        return pred_pseudo_tuples


    def _get_all_predictive_numbers_pseudonymize_sample_sheet(self):
        sample_sheet_path = os.path.join(self.run_path, "SampleSheet.csv")
        df = pd.read_csv(sample_sheet_path,
                         delimiter=",",
                         names=["[Header]", "Unnamed: 1", "Unnamed: 2", "Unnamed: 3", "Unnamed: 4",
                                "Unnamed: 5", "Unnamed: 6", "Unnamed: 7", "Unnamed: 8"])

        sample_list_header = df["[Header]"].to_list()
        sample_list_last = df["Unnamed: 8"].to_list()
        sample_ids_start = sample_list_header.index("Sample_ID") + 1

        predictive_numbers = sample_list_header[sample_ids_start:]
        predictive_pseudonimizer = PseudonymizePredictive(self.predictive_pseudo_table)
        pseudo_numbers = [predictive_pseudonimizer.pseudonymize(pred_number) for pred_number in predictive_numbers]

        new_column_header = sample_list_header[:sample_ids_start] + pseudo_numbers
        new_column_last = sample_list_last[:sample_ids_start] + pseudo_numbers

        df.drop(["[Header]", "Unnamed: 8"], axis=1, inplace=True)
        df.insert(loc=0, column="[Header]", value=new_column_header)
        df["Unnamed: 8"] = new_column_last
        df.columns = ["[Header]"] + ["" for _ in range(len(df.columns) - 1)]
        df.fillna("", inplace=True)
        df.to_csv(sample_sheet_path, header=False, index=False)

        predictive_pseudo_tuples = [(predictive_numbers[i], pseudo_numbers[i]) for i in range(len(predictive_numbers))]

        return predictive_pseudo_tuples