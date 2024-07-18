import requests
import os
import uuid
import logging
import json
import re
from ..helpers.config_processor import ConfigProcessor

class PseudonymizePredictive:

    def __init__(self,
                 path_to_predictive_pseudo_table_file):
        self.pseudo_table_file_path = path_to_predictive_pseudo_table_file
        self.predictive_pseudo_API = f"{ConfigProcessor().get_pseudo_API()}/predictive"


    def pseudonimize(self, pred_number) -> str:
        pseudo_number = self._check_if_already_has_pred_number(pred_number)
        if pseudo_number:
            return pseudo_number
        else:
            pseudo_number = self._generate_pseudo_number()
            self.__add_new_pseudo_number_to_file(pred_number, pseudo_number)
            self.__add_new_pseudo_number_to_db(pred_number, pseudo_number)
            return pseudo_number

    def _correct_pred_number_format(self, pred_number: str) -> str:
            # matching 2022-1234 ([whole_year]-[number])
        if re.match(r"^20[1-2][\d]-[\d]{1,4}", pred_number):
            year, id = pred_number.split("-", 1)
            return f"{id}-{year[2:]}"

        # matching 22-1234 ([year]-[number]) etc.
        if re.match(r"^[1-2][\d]\-[\d]{1,4}", pred_number):
            year, id = pred_number.split("-", 1)
            return f"{id}-{year}"

        # matching 1245-22 ([number]-[year]) etc.
        if re.match(r"^[\d]{1,4}\-[1-2][\d]", pred_number):
            return pred_number

        # matching 22_1234 ([year]_[number]) etc.
        if re.match(r"^[1-2][\d]_[\d]{1,4}", pred_number):
            year, id = pred_number.split("_", 1)
            return f"{id}-{year}"

        # matching 2022_1234 ([whole_year]_[number])
        if re.match(r"^20[1-2][\d]_[\d]{1,4}", pred_number):
            year, id = pred_number.split("_", 1)
            return f"{id}-{year[2:]}"

        return pred_number

    def _check_if_already_has_pred_number(self, pred_number):
        req = requests.get(f"{self.predictive_pseudo_API}/{pred_number}")
        if req.status_code == 200:
            data = req.json()
            if data:
                return data["predictive_pseudo_ID"]
            else:
                None


    def _generate_pseudo_number(self):
        return "mmci_predictive_" + str(uuid.uuid4())
    

    def __add_new_pseudo_number_to_file(self, predictive_number, pseudo_number):
        data = {"predictive":[]}
        if os.path.exists(self.pseudo_table_file_path):
            with open(self.pseudo_table_file_path, 'r') as json_file:
                data = json.load(json_file)
                pseudo_list = data["predictive"]
        else:
            pseudo_list = []

        with open(self.pseudo_table_file_path, 'w+') as output:
            sample = {"predictive_number": predictive_number, "pseudo_number": pseudo_number}
            pseudo_list.append(sample)
            data["predictive"] = pseudo_list
            json.dump(data, output, indent=4)
            logging.info("New predictive number was added to outputfile")


    def __add_new_pseudo_number_to_db(self, predictive_number, pseudo_number):
        new_data = {"predictive_ID": predictive_number, "predictive_pseudo_ID": pseudo_number}
        res = requests.post(f"{self.predictive_pseudo_API}", json=new_data)
        if res.status_code == 200:
            logging.info("New predictive number was sucessfully uploaded to DB with API")
        else:
            logging.warning(f"Could not upload new predictive_ID: {predictive_number} and its pseudonym: {pseudo_number}")