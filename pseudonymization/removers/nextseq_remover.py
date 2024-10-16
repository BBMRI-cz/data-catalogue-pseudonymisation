import os.path

from .remover import FileRemover
from pseudonymization.helpers.file_helpers import remove_path_if_exist


class NextSeqRemover(FileRemover):

    def __init__(self, sequencing_folder_path):
        self.folder_path = sequencing_folder_path

    def remove_files(self) -> None:
        paths_to_remove = [
            "Config",
            "Recipe",
            "Images",
            "Logs",
            "InstrumentAnalyticsLogs",
            "InterOp",
            "RTALogs",
            "CopyComplete.txt",
            "RTAComplete.txt",
            "RTARead1Complete.txt",
            "RTARead2Complete.txt",
            "RTARead3Complete.txt",
            "RTARead4Complete.txt",
        ]

        for path in paths_to_remove:
            remove_path_if_exist(os.path.join(self.folder_path, path))
