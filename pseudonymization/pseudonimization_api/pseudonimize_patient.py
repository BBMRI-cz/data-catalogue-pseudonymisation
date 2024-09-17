import requests
import os
import uuid
import logging
import json
from pseudonymization.config.config_processor import ConfigProcessor

class PseudonymizePatient:

    def __init__(self,
                 patient_number,
                 path_to_patient_pseudo_table_file):
        self.patient_number = patient_number
        self.pseudo_table_file_path = path_to_patient_pseudo_table_file
        self.patient_pseudo_API = f"{ConfigProcessor().get_pseudo_API()}/patient"


    def __call__(self) -> str:
        pseudo_number = self._check_if_already_has_patient_number()
        if pseudo_number:
            return pseudo_number
        else:
            pseudo_number = self._generate_patient_number()
            self.__add_new_patient_number_to_file(pseudo_number)
            self.__add_new_patient_number_to_db(pseudo_number)
            return pseudo_number


    def _check_if_already_has_patient_number(self):
        req = requests.get(f"{self.patient_pseudo_API}/{self.patient_number}")
        if req.status_code == 200:
            data = req.json()
            if data:
                return data["patient_pseudo_ID"]
            else:
                return None


    def _generate_patient_number(self):
        return "mmci_patient_" + str(uuid.uuid4())
    

    def __add_new_patient_number_to_file(self, pseudo_number):
        data = {"patients":[]}
        if os.path.exists(self.pseudo_table_file_path):
            with open(self.pseudo_table_file_path, 'r') as json_file:
                data = json.load(json_file)
                pseudo_list = data["patients"]
        else:
            pseudo_list = []

        with open(self.pseudo_table_file_path, 'w+') as output:
            sample = {"patient_ID": self.patient_number, "patient_pseudo_ID": pseudo_number}
            pseudo_list.append(sample)
            data["patients"] = pseudo_list
            json.dump(data, output, indent=4)
            logging.info("New patient_ID was added to outputfile")


    def __add_new_patient_number_to_db(self, pseudo_number):
        new_data = {"patient_ID": str(self.patient_number), "patient_pseudo_ID": pseudo_number}
        res = requests.post(f"{self.patient_pseudo_API}", json=new_data)
        if res.status_code == 200:
            logging.info("New patient number was sucessfully uploaded to DB with API")
        else:
            logging.warning(f"Could not upload new patient_ID: {self.patient_number} and its pseudonym: {pseudo_number}")