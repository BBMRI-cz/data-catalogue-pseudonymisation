from .Material import Material
from .Tissue import Tissue
from .Genome import Genome

from ..helpers.datetime_helpers import covert_to_date

class Serum(Material):
    """
    Child Class of Material defining the Serum

    Attributes
    ----------
    material : str
        "serum"
    diagnosis : str
        ICD-10 diagnosis of the tissue
    taking_date : str
        date when the serum was sampled from the patient in format (YYYY-MM-DD)
    """

    def __init__(self, sample_dict, pseudo_number, pseudo_sample_file):
        super().__init__(sample_dict, pseudo_number, pseudo_sample_file)
        self.material = sample_dict["type"]
        self.diagnosis = sample_dict["diagnosis"]
        self.taking_date = covert_to_date(sample_dict["taking_date"])

    def __lt__(self, other) -> bool:
        if isinstance(other, Tissue):
            return False
        if isinstance(other, Genome):
            return True
        if isinstance(other, Serum):
            return other.taking_date < self.taking_date
        
    def serialize(self) -> dict:
        sample_dict = super().serialize()
        sample_dict["material"] = self.material
        sample_dict["diagnosis"] = self.diagnosis
        sample_dict["taking_date"] = f"{self.taking_date.day}/{self.taking_date.month}/{self.taking_date.year}"
        return sample_dict