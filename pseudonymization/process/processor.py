import os
import shutil
import subprocess
import time
import  xml.etree.ElementTree as ET
from pathlib import Path

from pseudonymization.removers.remover import FileRemover
from pseudonymization.pseudonymizers.run_pseudonymizer import RunPseudonymizer
from pseudonymization.pseudonymizers.old_miseq_pseudonymizer import OldMiseqPseudonymizer
from pseudonymization.pseudonymizers.new_miseq_pseudonymizer import NewMiseqPseudonymizer
from pseudonymization.pseudonymizers.nextseq_pseudonymizer import NextSeqPseudonymizer

class Processor:

    def __init__(self, sequencing_run: str, destination_folder: str,
                 pseudo_tables_folder: str, sequencing_libraries: str, sequencing_libraries_sc: str):
        self.sequencing_file_path: str = sequencing_run
        self.destination_folder: str = destination_folder
        self.pseudonymization_tables_folder: str = pseudo_tables_folder
        self.sequencing_libraries_folder = sequencing_libraries
        self.sequencing_libraries_folder_sc = sequencing_libraries_sc

    def process_runs(self) -> None:
        for run in os.listdir(self.sequencing_file_path):
            print("PROCESSING RUN: ", run)
            full_run_path = os.path.join(self.sequencing_file_path, run)
            pseudonymizer = self._initialize_based_on_record_type(full_run_path)
            pseudonymizer.pseudonymize()
            self._mv_pseudonymizer_run_to_sc(run)

    def copy_libraries(self):
        self.touch_all_files(self.sequencing_libraries_folder)
        shutil.copytree(self.sequencing_libraries_folder, self.sequencing_libraries_folder_sc, dirs_exist_ok=True)

    def touch_all_files(self, directory):
        for root, dirs, files in os.walk(directory):
            for f in files:
                full_path = os.path.join(root, f)
                try:
                    subprocess.run(["touch", full_path], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"touch command failed: {e}")

    def _mv_pseudonymizer_run_to_sc(self, run_name):
        shutil.move(os.path.join(self.sequencing_file_path, run_name),
                    os.path.join(self.destination_folder, run_name))

    def _initialize_based_on_record_type(self, full_run_path) -> (FileRemover, RunPseudonymizer):
        if "SoftwareVersionsFile.csv" in os.listdir(full_run_path) or "Alignment_1" in os.listdir(full_run_path):
            pseudonymizer = NewMiseqPseudonymizer(full_run_path, self.pseudonymization_tables_folder)
        elif self._is_next_seq_based_on_run_parameters(full_run_path):
            pseudonymizer = NextSeqPseudonymizer(full_run_path, self.pseudonymization_tables_folder)
        else:
            pseudonymizer = OldMiseqPseudonymizer(full_run_path, self.pseudonymization_tables_folder)

        return pseudonymizer

    def _is_next_seq_based_on_run_parameters(self, full_run_path):
        run_parameters = os.path.join(full_run_path, "RunParameters.xml")
        if not os.path.exists(run_parameters):
            return False
        tree = ET.parse(run_parameters)
        root = tree.getroot()
        for child in root:
            if child.tag == "RunParametersVersion":
                return "nextseq" in child.text.lower()
