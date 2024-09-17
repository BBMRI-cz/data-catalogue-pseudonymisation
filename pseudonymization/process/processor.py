import os
import shutil

from pseudonymization.pseudonymizers.run_pseudonymizer import RunPseudonymizer
from pseudonymization.removers.remover import FileRemover
from pseudonymization.finders.info_finder import InfoFinder

from pseudonymization.pseudonymizers.old_miseq_pseudonymizer import OldMiseqPseudonymizer
from pseudonymization.pseudonymizers.new_miseq_pseudonymizer import NewMiseqPseudonymizer
from pseudonymization.pseudonymizers.nextseq_pseudonymizer import NextSeqPseudonymizer

from pseudonymization.removers.old_miseq_remover import OldMiSEQRemover
from pseudonymization.removers.new_miseq_remover import NewMiSEQRemover
from pseudonymization.removers.nextseq_remover import NextSeqRemover

from pseudonymization.finders.clinical_finder import ClinicalInfoFinder


class Processor:

    def __init__(self, sequencing_run: str, destination_folder: str, pseudo_tables_folder: str,
                 sequencing_libraries: str, sequencing_libraries_sc: str):
        self.sequencing_file_path: str = sequencing_run
        self.destination_folder: str = destination_folder
        self.pseudonymization_tables_folder: str = pseudo_tables_folder
        self.sequencing_libraries_folder = sequencing_libraries
        self.sequencing_libraries_folder_sc = sequencing_libraries_sc

    def process_runs(self) -> None:
        for run in os.listdir(self.sequencing_file_path):
            full_run_path = os.path.join(self.sequencing_file_path, run)
            pseudonymizer = self._initialize_based_on_record_type(full_run_path)

            pseudonymizer.pseudonymize()
            self._copy_pseudonymizer_run_to_sc(run)

    def copy_libraries(self):
        shutil.copytree(self.sequencing_libraries_folder, self.sequencing_libraries_folder_sc, dirs_exist_ok=True)

    def _copy_pseudonymizer_run_to_sc(self, run_name):
        shutil.move(os.path.join(self.sequencing_file_path, run_name),
                    os.path.join(self.destination_folder, run_name))

    def _initialize_based_on_record_type(self, full_run_path) -> (FileRemover, RunPseudonymizer):
        if "SoftwareVersionsFile.csv" in os.listdir(full_run_path) or "Alignment_1" in os.listdir(full_run_path):
            pseudonymizer = NewMiseqPseudonymizer(full_run_path, self.pseudonymization_tables_folder)
        elif "Something NextSeqSpecific" in os.listdir(full_run_path):
            pseudonymizer = NextSeqPseudonymizer()
        else:
            pseudonymizer = OldMiseqPseudonymizer(full_run_path, self.pseudonymization_tables_folder)

        return pseudonymizer
