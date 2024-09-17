from .remover import FileRemover


class NextSeqRemover(FileRemover):

    def __init__(self, sequencing_folder_path):
        self.folder_path = sequencing_folder_path

    def remove_files(self) -> None:
        pass
