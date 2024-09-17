from abc import ABC, abstractmethod


class RunPseudonymizer(ABC):

    @abstractmethod
    def pseudonymize(self):
        ...