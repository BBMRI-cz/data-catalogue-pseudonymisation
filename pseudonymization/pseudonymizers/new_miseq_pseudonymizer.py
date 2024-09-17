import os
import shutil
import subprocess
import logging

from .old_miseq_pseudonymizer import OldMiseqPseudonymizer
from pseudonymization.finders.clinical_finder import ClinicalInfoFinder
from pseudonymization.removers.new_miseq_remover import NewMiSEQRemover


class NewMiseqPseudonymizer(OldMiseqPseudonymizer):
    def __init__(self, run_path, pseudo_tables_folder_path):
        super().__init__(run_path, pseudo_tables_folder_path)

    def pseudonymize(self):
        pred_pseudo_tuples = self._get_all_predictive_numbers_pseudonymize_sample_sheet()
        self._move_alignmant_data_from_unknown_folder()
        NewMiSEQRemover(self.run_path).remove_files()

        for pred, pseudo in pred_pseudo_tuples:
            self._pseudonymize_files_with_pred_numbers(pred, pseudo)
            self._try_pseudonimize_content_of_files(pred, pseudo)
            clinical_data = ClinicalInfoFinder(self.run_path).collect_data(pred)

            if clinical_data:
                clinical_data_for_saving = self._prepare_clinical_data_for_saving(clinical_data, pseudo)
                self._save_clinical_data(clinical_data_for_saving,
                                         os.path.join(self.run_path, "catalog_info_per_pred_number"),
                                         pseudo)
                logging.debug(f"Clinical data saved to in catalog_inf_per_pred_number/{pseudo}")

    def _try_pseudonimize_content_of_files(self, pred_number, pseudo_pred_number):
        subprocess.call(["pseudonymization/helpers/replace_predictive_new_miseq.sh",
                        self.run_path,
                        pred_number,
                        pseudo_pred_number])

    def _move_alignmant_data_from_unknown_folder(self):
        old_folder = os.path.join(self.run_path, "Alignment_1", self._find_folder_names_in_alignment())
        new_folder = os.path.join(self.run_path, "Alignment_1")
        for file in os.listdir(old_folder):
            shutil.move(os.path.join(old_folder, file), os.path.join(new_folder, file))
        os.rmdir(old_folder)

    def _find_folder_names_in_alignment(self) -> str:
        paths_in_alignment = [file for file in os.listdir(os.path.join(self.run_path, "Alignment_1"))
                              if os.path.isdir(os.path.join(self.run_path, "Alignment_1", file))]
        if len(paths_in_alignment) > 0:
            return paths_in_alignment[0]
        else:
            return ""
