from .Material import Material

from ..helpers.datetime_helpers import covert_str_to_datetime


class Patient:
    """
    Class defining an pseudonimized patient that gave concent to the 
    BBM of MMCI that his material and data can be used for research

    Attributes
    ----------
    ID  : str
        randomly generated (UUID v4)
    birth : str
        birth month and year of the patient
    sex : str
        biological sex of the patient
    samples : List[Material]
        list of materials that belong to the patient
    """

    def __init__(self, id: str, birth: str, sex: str, samples: list[Material]):
        self.ID = id
        self.birth = covert_str_to_datetime(birth)
        self.sex = sex
        self.samples = samples

    def __eq__(self, other):
        if isinstance(other, Patient):
            return self.ID == other.ID
        return False
    
    def serialize(self):
        return {
            "ID": self.ID,
            "birth": self.birth.strftime("%d/%m/%Y"),
            "sex": self.sex,
            "samples": [sample.serialize() for sample in self.samples]
        }
    
    