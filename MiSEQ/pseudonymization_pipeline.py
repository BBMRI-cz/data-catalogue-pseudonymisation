import argparse
import os 
import shutil

from pseudonymization.Pseudonimizer import RunPseudonimizer


def remove_path_if_exist(file_path):
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)

def remove_run_files(run_path):
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

def copy_if_not_exist(old_path, new_path):
    if not os.path.exists(new_path):
        shutil.copytree(old_path, new_path)

def pseudonymize_runs(source_folder, destination_folder, pseudo_samples_folder, sequencing_libraries):
    for run in os.listdir(source_folder):
        run_path = os.path.join(source_folder, run)
        remove_run_files(run_path)
        RunPseudonimizer(run_path, pseudo_samples_folder)()
        copy_if_not_exist(run_path, os.path.join(destination_folder, run))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Sequencing Pseudonymization",
                                     description="This script pseudonymized the data, deletes unimportant data and seconds them to SensitiveCloud")
    parser.add_argument("source_folder")
    parser.add_argument("destination_folder")
    parser.add_argument("pseudo_tables_folder")
    parser.add_argument("sequencing_libraries")
    
    args = parser.parse_args()
    
    pseudonymize_runs(args.source_folder, args.destination_folder, args.pseudo_tables_folder, args.sequencing_libraries)






