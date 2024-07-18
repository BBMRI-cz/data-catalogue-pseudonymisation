from .Material import Material

from ..helpers.datetime_helpers import covert_to_date

class Genome(Material):
    """
    Child Class of Material defining the Genome

    Attributes
    ----------
    material : str
        "serum"
    taking_date : datetime
        date when the genome was sampled from the patient in format (YYYY-MM-DD)
    """

    def __init__(self, sample_dict, pseudo_number,  sample_table):
        super().__init__(sample_dict, pseudo_number,  sample_table)
        self.material = sample_dict["type"]
        self.retrieved = sample_dict["retrieved"]
        self.taking_date = covert_to_date(sample_dict["taking_date"])

    def __lt__(self, other) -> bool:
        if isinstance(other, Genome):
            return other.taking_date < self.taking_date
        return False
    
    def serialize(self) -> dict:
        sample_dict = super().serialize()
        sample_dict["material"] = self.material
        sample_dict["retrieved"] = self.retrieved
        sample_dict["taking_date"] = f"{self.taking_date.day}/{self.taking_date.month}/{self.taking_date.year}"
        return sample_dict