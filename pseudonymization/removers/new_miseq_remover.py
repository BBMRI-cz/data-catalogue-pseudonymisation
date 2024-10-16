import os.path
from .remover import FileRemover
from pseudonymization.helpers.file_helpers import remove_path_if_exist


class NewMiSEQRemover(FileRemover):

    def __init__(self, sequencing_file_path):
        self.sequencing_run_file_path = sequencing_file_path

    def remove_files(self) -> None:
        paths_to_remove = [
            os.path.join("Data", "RTALogs"),
            os.path.join("Data", "Intensities", "L001"),
            "Thumbnail_Images",
            os.path.join("Data", "Intensities", "RTAConfiguration.xml"),
            os.path.join("Alignment_1", "SampleSheetUsed.csv"),
            os.path.join("Alignment_1", "GenerateFASTQRunStatistics.xml"),
            "Basecalling_Netcopy_complete_Read1.txt",
            "Basecalling_Netcopy_complete_Read2.txt",
            "ImageAnalysis_Netcopy_complete_Read1.txt",
            "ImageAnalysis_Netcopy_complete_Read2.txt",
            "RTAComplete.txt",
            "QueuedForAnalysis.txt",
            "Recipe"
        ]

        for file_path in paths_to_remove:
            remove_path_if_exist(os.path.join(self.sequencing_run_file_path, file_path))
