import pytest
import os
import shutil
from pseudonymization.pseudonymizers.new_miseq_pseudonymizer import NewMiseqPseudonymizer


tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

FAKE_RUN_FOLDER_FOR_COPY = os.path.join(tests_dir, "new_miseq_test_run")
FAKE_RUN_FOR_TESTING = os.path.join(tests_dir, "FAKE_RUN")

PSEUDONYMIZATION_FILES_FOLDER = os.path.join(tests_dir, "pseudonymization_files")
PSEUDONYMIZATION_PATIENTS_FILE = os.path.join(PSEUDONYMIZATION_FILES_FOLDER, "patients.json")
PSEUDONYMIZATION_SAMPLES_FILE = os.path.join(PSEUDONYMIZATION_FILES_FOLDER, "samples.json")
PSEUDONYMIZATION_PREDICTIVE_FILE = os.path.join(PSEUDONYMIZATION_FILES_FOLDER, "predictive.json")


def test_move_files_inside_alignment(mocker, uuid_generated_values):
    mocker.patch("pseudonymization.pseudonymizers.new_miseq_pseudonymizer.subprocess.call",
                 side_effects=mocker.Mock())
    mocker.patch("pseudonymization.pseudonymizers.new_miseq_pseudonymizer.ClinicalInfoFinder.collect_data",
                 return_value=[])
    mocker.patch("pseudonymization.pseudonymizers.old_miseq_pseudonymizer.PseudonymizePredictive.pseudonymize",
                 side_effect=uuid_generated_values)
    pseudonymizer = NewMiseqPseudonymizer(
        FAKE_RUN_FOR_TESTING,
        PSEUDONYMIZATION_FILES_FOLDER)
    pseudonymizer.pseudonymize()

    assert os.path.exists(os.path.join(FAKE_RUN_FOR_TESTING,
                                       "Alignment_1"))


def test_rename_files_recursively(mocker, uuid_generated_values):
    mocker.patch("pseudonymization.pseudonymizers.new_miseq_pseudonymizer.subprocess.call",
                 side_effects=mocker.Mock())
    mocker.patch("pseudonymization.pseudonymizers.new_miseq_pseudonymizer.ClinicalInfoFinder.collect_data",
                 return_value=[])
    mocker.patch("pseudonymization.pseudonymizers.old_miseq_pseudonymizer.PseudonymizePredictive.pseudonymize",
                 side_effect=uuid_generated_values)
    pseudonymizer = NewMiseqPseudonymizer(
        FAKE_RUN_FOR_TESTING,
        PSEUDONYMIZATION_FILES_FOLDER)
    pseudonymizer.pseudonymize()

    assert os.path.exists(os.path.join(FAKE_RUN_FOR_TESTING,
                                       "Alignment_1",
                                       "Fastq",
                                       "mmci_predictive_12345678-1234-5678-1234-567812345601_S1_L001_R1_001.fastq.gz"))


def test_clinical_info_folder_created(mocker, uuid_generated_values, get_test_patient):
    mocker.patch("pseudonymization.pseudonymizers.new_miseq_pseudonymizer.subprocess.call",
                 side_effects=mocker.Mock())
    mocker.patch("pseudonymization.pseudonymizers.old_miseq_pseudonymizer.PseudonymizePredictive.pseudonymize",
                 side_effect=uuid_generated_values)
    mocker.patch("pseudonymization.pseudonymizers.old_miseq_pseudonymizer.PseudonymizePatient.__call__",
                 side_effect=uuid_generated_values)
    mocker.patch("pseudonymization.pseudonymizers.new_miseq_pseudonymizer.ClinicalInfoFinder.collect_data",
                 return_value=get_test_patient)

    pseudonymizer = NewMiseqPseudonymizer(
        FAKE_RUN_FOR_TESTING,
        PSEUDONYMIZATION_FILES_FOLDER)
    pseudonymizer.pseudonymize()

    assert os.path.exists(os.path.join(FAKE_RUN_FOR_TESTING,
                                       "catalog_info_per_pred_number",
                                       "mmci_predictive_12345678-1234-5678-1234-567812345600.json"))


def _setup_pseudonymization_files():
    os.mkdir(PSEUDONYMIZATION_FILES_FOLDER)


def _copy_fake_run():
    shutil.copytree(FAKE_RUN_FOLDER_FOR_COPY, FAKE_RUN_FOR_TESTING)


def _teardown_pseudonymization_files():
    shutil.rmtree(PSEUDONYMIZATION_FILES_FOLDER)


def _remove_coppied_fake_run():
    shutil.rmtree(FAKE_RUN_FOR_TESTING)


@pytest.fixture(autouse=True)
def setup_and_teardown_pseodonymization_files(request):
    _setup_pseudonymization_files()
    _copy_fake_run()

    request.addfinalizer(_teardown_pseudonymization_files)
    request.addfinalizer(_remove_coppied_fake_run)


@pytest.fixture
def uuid_generated_values():
    return ["mmci_predictive_12345678-1234-5678-1234-5678123456" + "{:02d}".format(number)
            for number in range(0, 19)]


@pytest.fixture
def get_test_patient():
    return {
        "ID": "0000",
        "birth_date": "Sun, 01 Aug 1948 00:00:00 GMT",
        "sex": 2,
        "samples": []
    }
