import os
import shutil
import pytest
from pseudonymization.pseudonymizers.nextseq_pseudonymizer import NextSeqPseudonymizer

tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

FAKE_RUN_FOLDER_FOR_COPY = os.path.join(tests_dir, "next_seq_test_run")
FAKE_RUN_FOR_TESTING = os.path.join(tests_dir, "FAKE_RUN")

PSEUDONYMIZATION_FILES_FOLDER = os.path.join(tests_dir, "pseudonymization_files")
PSEUDONYMIZATION_PATIENTS_FILE = os.path.join(PSEUDONYMIZATION_FILES_FOLDER, "patients.json")
PSEUDONYMIZATION_SAMPLES_FILE = os.path.join(PSEUDONYMIZATION_FILES_FOLDER, "samples.json")
PSEUDONYMIZATION_PREDICTIVE_FILE = os.path.join(PSEUDONYMIZATION_FILES_FOLDER, "predictive.json")

EXPECTED_PSEUDO_TUPLES = [('2000_0000_DNA', 'mmci_predictive_12345678-1234-5678-1234-567812345600'),
 ('2000_0001_DNA', 'mmci_predictive_12345678-1234-5678-1234-567812345601'),
 ('2000_0002_DNA', 'mmci_predictive_12345678-1234-5678-1234-567812345602'),
 ('2000_0003_DNA', 'mmci_predictive_12345678-1234-5678-1234-567812345603'),
 ('2000_0004_DNA', 'mmci_predictive_12345678-1234-5678-1234-567812345604'),
 ('2000_0005_DNA', 'mmci_predictive_12345678-1234-5678-1234-567812345605'),
 ('2000_0006_DNA', 'mmci_predictive_12345678-1234-5678-1234-567812345606'),
 ('ST20-00_DNA', 'mmci_predictive_12345678-1234-5678-1234-567812345607'),
 ('2000_0007_RNA', 'mmci_predictive_12345678-1234-5678-1234-567812345608'),
 ('2000_0008_RNA', 'mmci_predictive_12345678-1234-5678-1234-567812345609'),
 ('2000_0009_RNA', 'mmci_predictive_12345678-1234-5678-1234-567812345610'),
 ('2000_0010_RNA', 'mmci_predictive_12345678-1234-5678-1234-567812345611'),
 ('2000_0011_RNA', 'mmci_predictive_12345678-1234-5678-1234-567812345612'),
 ('2000_0012_RNA', 'mmci_predictive_12345678-1234-5678-1234-567812345613'),
 ('2000_0013_RNA', 'mmci_predictive_12345678-1234-5678-1234-567812345614'),
 ('ST20-01_DNA', 'mmci_predictive_12345678-1234-5678-1234-567812345615')]

def test_sample_sheet_pseudonymized(mock_pseudonymize_predictive):
    values = NextSeqPseudonymizer(FAKE_RUN_FOR_TESTING, PSEUDONYMIZATION_FILES_FOLDER).pseudonymize()

    assert values == EXPECTED_PSEUDO_TUPLES


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
def mock_pseudonymize_predictive(mocker, uuid_generated_values):
    mocker.patch("pseudonymization.pseudonymizers.nextseq_pseudonymizer.PseudonymizePredictive.pseudonymize",
                 side_effect=uuid_generated_values)
