import requests
import os
import uuid
import logging
import json
from ..helpers.config_processor import ConfigProcessor

class PseudonymizeSample:

    def __init__(self,
                 sample_number,
                 path_to_sample_pseudo_table_file):
        self.sample_number = sample_number
        self.pseudo_table_file_path = path_to_sample_pseudo_table_file
        self.sample_pseudo_API = f"{ConfigProcessor().get_pseudo_API()}/sample"


    def __call__(self) -> str:
        pseudo_number = self._check_if_already_has_sample_number()
        if pseudo_number:
            return pseudo_number
        else:
            pseudo_number = self._generate_sample_number()
            self.__add_new_sample_number_to_file(pseudo_number)
            self.__add_new_sample_number_to_db(pseudo_number)
            return pseudo_number


    def _check_if_already_has_sample_number(self):
        req = requests.get(f"{self.sample_pseudo_API}/{self.sample_number}")
        if req.status_code == 200:
            data = req.json()
            if data:
                return data["sample_pseudo_ID"]
            else:
                None


    def _generate_sample_number(self):
        return "mmci_sample_" + str(uuid.uuid4())
    

    def __add_new_sample_number_to_file(self, pseudo_number):
        data = {"samples":[]}
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
            logging.info("New sample_ID was added to outputfile")


    def __add_new_sample_number_to_db(self, pseudo_number):
        new_data = {"sample_ID": self.sample_number, "pseudo_sample_ID": pseudo_number}
        res = requests.post(f"{self.sample_pseudo_API}", json=new_data)
        print(res)
        if res.status_code == 200:
            logging.info("New patient number was sucessfully uploaded to DB with API")
        else:
            logging.warning(f"Could not upload new sample_ID: {self.sample_number} and its pseudonym: {pseudo_number}")