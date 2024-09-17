import os
import shutil


def remove_path_if_exist(file_path):
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)


def remove_miseq_run_files(run_path: object) -> object:
    remove_path_if_exist(os.path.join(run_path, "Data", "RTALogs"))
    remove_path_if_exist(os.path.join(run_path, "Data", "Intensities", "L001"))
    remove_path_if_exist(os.path.join(run_path, "Thumbnail_Images"))
    remove_path_if_exist(os.path.join(run_path, "Recipe"))
    remove_path_if_exist(os.path.join(run_path, "Data", "Intensities", "RTAConfiguration.xml"))
    remove_path_if_exist(os.path.join(run_path, "Data", "Intensities", "BaseCalls", "SampleSheet.csv"))                                
    remove_path_if_exist(os.path.join(run_path, "Data", "Intensities", "BaseCalls", "Alignment", "SampleSheetUsed.csv"))
    remove_path_if_exist(os.path.join(run_path, "Data", "Intensities", "BaseCalls", "Alignment", "GenerateFASTQRunStatistics.xml"))
    remove_path_if_exist(os.path.join(run_path, "Basecalling_Netcopy_complete_Read1.txt"))                    
    remove_path_if_exist(os.path.join(run_path, "Basecalling_Netcopy_complete_Read2.txt"))
    remove_path_if_exist(os.path.join(run_path, "Basecalling_Netcopy_complete_Read3.txt"))
    remove_path_if_exist(os.path.join(run_path, "Basecalling_Netcopy_complete_Read4.txt"))
    remove_path_if_exist(os.path.join(run_path, "ImageAnalysis_Netcopy_complete_Read1.txt"))
    remove_path_if_exist(os.path.join(run_path, "ImageAnalysis_Netcopy_complete_Read2.txt"))
    remove_path_if_exist(os.path.join(run_path, "ImageAnalysis_Netcopy_complete_Read3.txt"))
    remove_path_if_exist(os.path.join(run_path, "ImageAnalysis_Netcopy_complete_Read4.txt"))
    remove_path_if_exist(os.path.join(run_path, "QueuedForAnalysis.txt"))
    remove_path_if_exist(os.path.join(run_path, "RTAComplete.txt"))


def remove_nextseq_run_files(run_path):
    pass

def mv_if_source_not_exist(old_path, new_path):
    if not os.path.exists(new_path):
        shutil.copytree(old_path, new_path)
        shutil.rmtree(old_path)