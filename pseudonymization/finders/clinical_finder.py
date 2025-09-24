import requests
import re
from pseudonymization.config.config_processor import ConfigProcessor
from pseudonymization.logging_config.logging_config import LoggingConfig


class ClinicalInfoFinder:

    def __init__(self, run_path: str):
        self.run_path = run_path
        self.EXPORT_API = ConfigProcessor().get_export_API()
        self.logger = LoggingConfig.get_logger()

    def collect_data(self, predictive_number: str) -> dict | None:
        fixed_pred_number = self._fix_pred_number_format_for_export(predictive_number)  # 2022-1234 format
        if fixed_pred_number:
            clinical_data = self._get_clinical_data_from_pred_number(fixed_pred_number)
            if clinical_data:
                self.logger.info(f"Clinical data found for predictive number {predictive_number}")
                patient_id = clinical_data[0]["patient_id"]
                patient = self._get_patient_dict_based_on_sample_data(patient_id)
                if patient:
                    self.logger.info(f"Patient info found for patient id {patient_id}")
                    patient["samples"] = clinical_data
                    return patient
                else:
                    self.logger.info(f"No patient info found for patient id {patient_id}, skipping clinical data")
            else:
                self.logger.info(f"No clinical data found for predictive number {predictive_number}")
        return None

    def _fix_pred_number_format_for_export(self, pred_number: str) -> str | None:

        # matching 2022-1234 ([whole_year]-[number])
        if re.match(r"^20[1-2][\d]\-[\d]{1,4}$", pred_number):
            return pred_number

        # matching 22-1234 ([year]-[number]) etc.
        if re.match(r"^[1-2][\d]\-[\d]{1,4}$", pred_number):
            year, id = pred_number.split("-", 1)
            return f"20{year}-{id}"

        # matching 1245-22 ([number]-[year]) etc.
        if re.match(r"^[\d]{1,4}\-[1-2][\d]$", pred_number):
            id, year = pred_number.split("-", 1)
            return f"20{year}-{id}"

        # matching 22_1234 ([year]_[number]) etc.
        if re.match(r"^[1-2][\d]_[\d]{1,4}$", pred_number):
            year, id = pred_number.split("_", 1)
            return f"20{year}-{id}"

        # matching 2022_1234 ([whole_year]_[number])
        if re.match(r"^20[1-2][\d]_[\d]{1,4}$", pred_number):
            return pred_number.replace("_", "-")

        return None

    def _get_clinical_data_from_pred_number(self, pred_number: str) -> dict | None:
        res = requests.get(f"{self.EXPORT_API}/specimen/{pred_number}")
        if res.status_code == 200:
            data = res.json()
            if data:
                return data
            else: 
                return None
        else:
            return None
        
    def _get_patient_dict_based_on_sample_data(self, patient_id: str) -> dict | None:
        res = requests.get(f"{self.EXPORT_API}/patient/{patient_id}")
        if res.status_code == 200:
            data = res.json()
            return data
        else:
            return None
