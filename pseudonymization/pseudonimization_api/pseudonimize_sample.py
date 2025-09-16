import requests
import os
import uuid
import json
from pseudonymization.config.config_processor import ConfigProcessor
from pseudonymization.logging_config.logging_config import LoggingConfig


class PseudonymizeSample:

    def __init__(self,
                 sample_number,
                 path_to_sample_pseudo_table_file):
        self.sample_number = sample_number
        self.pseudo_table_file_path = path_to_sample_pseudo_table_file
        self.sample_pseudo_API = f"{ConfigProcessor().get_pseudo_API()}/sample"
        self.logger = LoggingConfig.get_logger()

    def __call__(self) -> str:
        pseudo_sample_number = self._check_if_already_has_sample_number()
        if pseudo_sample_number:
            return pseudo_sample_number
        else:
            pseudo_sample_number = self._generate_sample_number()
            self.__add_new_sample_number_to_file(pseudo_sample_number)
            self.__add_new_sample_number_to_db(pseudo_sample_number)
            return pseudo_sample_number

    def _check_if_already_has_sample_number(self):
        req = requests.get(f"{self.sample_pseudo_API}/{self.sample_number}")
        if req.status_code == 200:
            data = req.json()
            if data:
                return data["sample_pseudo_ID"]
            else:
                return None

    def _generate_sample_number(self):
        return "mmci_sample_" + str(uuid.uuid4())

    def __add_new_sample_number_to_file(self, pseudo_number):
        data = {"samples": []}
        if os.path.exists(self.pseudo_table_file_path):
            with open(self.pseudo_table_file_path, 'r') as json_file:
                data = json.load(json_file)
                pseudo_list = data["samples"]
        else:
            pseudo_list = []

        with open(self.pseudo_table_file_path, 'w+') as output:
            sample = {"sample_ID": self.sample_number, "pseudo_sample_ID": pseudo_number}
            pseudo_list.append(sample)
            data["samples"] = pseudo_list
            json.dump(data, output, indent=4)
            self.logger.info("New sample_ID was added to outputfile")

    def __add_new_sample_number_to_db(self, pseudo_number):
        new_data = {"sample_ID": self.sample_number, "pseudo_sample_ID": pseudo_number}
        res = requests.post(f"{self.sample_pseudo_API}", json=new_data)
        if res.status_code == 200:
            self.logger.info("New patient number was sucessfully uploaded to DB with API")
        else:
            self.logger.warning(f"Could not upload new sample_ID: {self.sample_number} and its pseudonym: {pseudo_number}")
