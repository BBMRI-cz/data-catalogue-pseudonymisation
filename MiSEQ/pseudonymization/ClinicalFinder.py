import requests
import re
from .ConfigProcessor import ConfigProcessor


class ClinicalInfoFinder:

    def __init__(self, run_path: str):
        self.run_path = run_path
        self.EXPORT_API = ConfigProcessor().get_export_API()

    def collect_clinical_data(self, predictive_number: str) -> dict:
        fixed_pred_number = self._fix_pred_number_format_for_export(predictive_number) # 2022-1234 format
        print("Fixed pred number:", fixed_pred_number)
        if fixed_pred_number:
            clinical_data = self._get_clinical_data_from_pred_number(fixed_pred_number)
            if clinical_data:
                patient = self._get_patient_dict_based_on_sample_data(clinical_data)
                patient["samples"] = clinical_data
                print("Number of data found for patient:",  len(patient["samples"]))
                return patient
        return None


    def _fix_pred_number_format_for_export(self, pred_number: str) -> str:

        # matching 2022-1234 ([whole_year]-[number])
        if re.match(r"^20[1-2][\d]-[\d]{1,4}", pred_number):
            return pred_number

        # matching 22-1234 ([year]-[number]) etc.
        if re.match(r"^[1-2][\d]\-[\d]{1,4}", pred_number):
            year, id = pred_number.split("-", 1)
            return f"20{year}-{id}"

        # matching 1245-22 ([number]-[year]) etc.
        if re.match(r"^[\d]{1,4}\-[1-2][\d]", pred_number):
            id, year = pred_number.split("-", 1)
            return f"20{year}-{id}"

        # matching 22_1234 ([year]_[number]) etc.
        if re.match(r"^[1-2][\d]_[\d]{1,4}", pred_number):
            year, id = pred_number.split("_", 1)
            return f"20{year}-{id}"

        # matching 2022_1234 ([whole_year]_[number])
        if re.match(r"^20[1-2][\d]_[\d]{1,4}", pred_number):
            return pred_number.replace("_", "-")

        return None
    

    def _get_clinical_data_from_pred_number(self, pred_number: str) -> dict:
        res = requests.get(f"{self.EXPORT_API}/specimen/{pred_number}")
        if res.status_code == 200:
            data = res.json()
            if data:
                return data
            else: 
                return None
        else:
            return None
        
    def _get_patient_dict_based_on_sample_data(self, sample_data: dict) -> dict:
        patient_id = sample_data[0]["patient_id"]
        res = requests.get(f"{self.EXPORT_API}/patient/{patient_id}")
        if res.status_code == 200:
            data = res.json()
            return data
        else:
            return None