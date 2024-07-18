from ..pseudonimization_api.pseudonimize_sample import PseudonymizeSample

class Material:
    """
    Parent class for all the different materials present in the LTS (Long term Storage) of MMCI Biobank

    Attributes
    ----------
    pseudo_ID : str
        randomly generated (UUID v4) pseudo_ID (originally predictive number)
    biopsy_number : str
        if the sample underwent a biopsy an unique number of that biopsy is assigned
    sample_ID :  str
        randomly generated (UUID v4) sample_ID
    sample_number: str
        number of the sample stored
    available_samples_number: str
        number of available sample stored
    material_type: str 
        an integer defining what type of material is the sample
    """


    def __init__(self, sample_dict, pseudo_number, pseudo_sample_file):
        self.pseudo_ID = pseudo_number
        self.biopsy_number = sample_dict["biopsy_id"]
        self.sample_ID = PseudonymizeSample(sample_dict["sample_id"], pseudo_sample_file)()
        self.sample_number = sample_dict["samples_no"]
        self.available_samples_number = sample_dict["available_samples_no"]
        self.material_type = sample_dict["material_type_id"]

    def __eq__(self, other) -> bool:
        if isinstance(other, Material):
            return self.sample_ID == other.sample_ID
        return False

    def __hash__(self) -> int:
        return hash(("sample_id", self.sample_ID))

    def __str__(self) -> str:
        return f"{self.sample_ID}"
    
    def serialize(self) -> dict:
        return {
            "pseudo_ID": self.pseudo_ID,
            "biopsy_number": self.biopsy_number,
            "sample_ID": self.sample_ID,
            "sample_number": self.sample_number,
            "available_samples_number": self.available_samples_number,
            "material_type": self.material_type,
        }