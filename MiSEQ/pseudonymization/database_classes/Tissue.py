from .Material import Material
from ..helpers.datetime_helpers import covert_to_date


class Tissue(Material):
    """
    Child Class of Material defining the Tissue

    Attributes
    ----------
    material : str
        "tissue"
    pTNM : str
        TNM-7 of the tissue
    morphology : str
        ICD-03 morphology part of the tissue
    diagnosis : str
        ICD-10 diagnosis of the tissue
    cut_time : str
        time the tissue was cut from the patient in format (YYYY-MM-DDTHH:MM:SS)
    freeze_time : str
        time the tissue was frozen in format (YYYY-MM-DDTHH:MM:SS)
    retrieved : str
        Method specifiing how the tissue was retrieved from the patient
    """

    def __init__(self, sample_dict, pseudo_number, sample_table):
        super().__init__(sample_dict, pseudo_number, sample_table)
        self.material = sample_dict["type"]
        self.pTNM = sample_dict["ptnm"]
        self.morphology = sample_dict["morphology"]
        self.diagnosis = sample_dict["diagnosis"]
        self.cut_time = covert_to_date(sample_dict["cut_time"])
        self.freeze_time = covert_to_date(sample_dict["freeze_time"])
        self.retrieved = sample_dict["retrieved"]

    def __str__(self) -> str:
        return f"{self.sample_ID}"

    def __repr__(self) -> str:
        return f"{self.sample_ID}"
    
    def __lt__(self, other) -> bool:
        if isinstance(other, Tissue):
            return int(self.material_type) < int(other.material_type)
        return True
    
    def serialize(self) -> dict:
        sample_dict =  super().serialize()
        sample_dict["material"] = self.material
        sample_dict["pTNM"] = self.pTNM
        sample_dict["morphology"] = self.morphology
        sample_dict["diagnosis"] = self.diagnosis
        sample_dict["cut_time"] = f"{self.cut_time.date} {self.cut_time.time}"
        sample_dict["freeze_time"] = f"{self.freeze_time.date} {self.freeze_time.time}"
        sample_dict["retrieved"] = self.retrieved
        return sample_dict