from .remover import FileRemover
import os
from pseudonymization.helpers.file_helpers import remove_path_if_exist


class OldMiSEQRemover(FileRemover):

    def __init__(self, sequencing_run_path):
        self.run_path = sequencing_run_path

    def remove_files(self) -> None:
        remove_path_if_exist(os.path.join(self.run_path, "Data", "RTALogs"))
        remove_path_if_exist(os.path.join(self.run_path, "Data", "Intensities", "L001"))
        remove_path_if_exist(os.path.join(self.run_path, "Thumbnail_Images"))
        remove_path_if_exist(os.path.join(self.run_path, "Recipe"))
        remove_path_if_exist(os.path.join(self.run_path, "Data", "Intensities", "RTAConfiguration.xml"))
        remove_path_if_exist(os.path.join(self.run_path, "Data", "Intensities", "BaseCalls", "SampleSheet.csv"))
        remove_path_if_exist(os.path.join(self.run_path, "Data", "Intensities", "BaseCalls",
                                          "Alignment", "SampleSheetUsed.csv"))
        remove_path_if_exist(os.path.join(self.run_path, "Data", "Intensities", "BaseCalls",
                                          "Alignment", "GenerateFASTQRunStatistics.xml"))
        remove_path_if_exist(os.path.join(self.run_path, "Basecalling_Netcopy_complete_Read1.txt"))
        remove_path_if_exist(os.path.join(self.run_path, "Basecalling_Netcopy_complete_Read2.txt"))
        remove_path_if_exist(os.path.join(self.run_path, "Basecalling_Netcopy_complete_Read3.txt"))
        remove_path_if_exist(os.path.join(self.run_path, "Basecalling_Netcopy_complete_Read4.txt"))
        remove_path_if_exist(os.path.join(self.run_path, "ImageAnalysis_Netcopy_complete_Read1.txt"))
        remove_path_if_exist(os.path.join(self.run_path, "ImageAnalysis_Netcopy_complete_Read2.txt"))
        remove_path_if_exist(os.path.join(self.run_path, "ImageAnalysis_Netcopy_complete_Read3.txt"))
        remove_path_if_exist(os.path.join(self.run_path, "ImageAnalysis_Netcopy_complete_Read4.txt"))
        remove_path_if_exist(os.path.join(self.run_path, "QueuedForAnalysis.txt"))
        remove_path_if_exist(os.path.join(self.run_path, "RTAComplete.txt"))
