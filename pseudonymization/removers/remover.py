from abc import ABC, abstractmethod


class FileRemover(ABC):

    @abstractmethod
    def remove_files(self):
        ...
