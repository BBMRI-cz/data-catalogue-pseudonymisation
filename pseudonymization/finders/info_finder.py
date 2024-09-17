from abc import ABC, abstractmethod


class InfoFinder(ABC):

    @abstractmethod
    def collect_data(self):
        ...
