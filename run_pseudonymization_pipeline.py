import argparse
import os 
import shutil

from pseudonymization.helpers.file_helpers import remove_miseq_run_files, remove_nextseq_run_files, mv_if_source_not_exist
from pseudonymization.process.pseudonimizer import RunPseudonimizer


def pseudonymize_miseq_runs(source_folder, destination_folder, pseudo_samples_folder, sequencing_libraries, sc_libraries):
    shutil.copytree(sequencing_libraries, sc_libraries, dirs_exist_ok=True)
    for run in os.listdir(source_folder):
        run_path = os.path.join(source_folder, run)
        remove_miseq_run_files(run_path)
        RunPseudonimizer(run_path, pseudo_samples_folder)()
        mv_if_source_not_exist(run_path, os.path.join(destination_folder, run))


def pseudonymize_nextseq_runs(source_folder, destination_folder, pseudo_samples_folder, sequencing_libraries, sc_libraries):
    shutil.copytree(sequencing_libraries, sc_libraries, dirs_exist_ok=True)
    for run in os.listdir(source_folder):
        run_path = os.path.join(source_folder, run)
        remove_nextseq_run_files(run_path)
        RunPseudonimizer(run_path, pseudo_samples_folder)()
        mv_if_source_not_exist(run_path, os.path.join(destination_folder, run))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Sequencing Pseudonymization",
                                     description="This script pseudonymized the data, deletes unimportant data and seconds them to SensitiveCloud")
    parser.add_argument("source_folder")
    parser.add_argument("destination_folder")
    parser.add_argument("pseudo_tables_folder")
    parser.add_argument("sequencing_libraries")
    parser.add_argument("sequencing_libraries_sc")
    parser.add_argument("run_type", choices=["MiSEQ", "NextSeq"])
    
    args = parser.parse_args()
    
    if args.run_type == "MiSEQ":
        pseudonymize_miseq_runs(args.source_folder,
                                args.destination_folder,
                                args.pseudo_tables_folder,
                                args.sequencing_libraries,
                                args.sequencing_libraries_sc)
        print("DONE")
    elif args.run_type == "NextSeq":
        pseudonymize_nextseq_runs(args.source_folder, args.destination_folder, args.pseudo_tables_folder, args.sequencing_libraries, args.sequencing_libraries_sc)