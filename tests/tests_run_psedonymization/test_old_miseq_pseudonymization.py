import pytest
import os
import shutil
from pseudonymization.pseudonymizers.old_miseq_pseudonymizer import OldMiseqPseudonymizer
from pseudonymization.models.Patient import Patient
from pseudonymization.models.Material import Material
from pseudonymization.models.Tissue import Tissue
from pseudonymization.models.Serum import Serum

tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

FAKE_RUN_FOLDER_FOR_COPY = os.path.join(tests_dir, "old_miseq_test_run")
FAKE_RUN_FOR_TESTING = os.path.join(tests_dir, "FAKE_RUN")

PSEUDONYMIZATION_FILES_FOLDER = os.path.join(tests_dir, "pseudonymization_files")
PSEUDONYMIZATION_PATIENTS_FILE = os.path.join(PSEUDONYMIZATION_FILES_FOLDER, "patients.json")
PSEUDONYMIZATION_SAMPLES_FILE = os.path.join(PSEUDONYMIZATION_FILES_FOLDER, "samples.json")
PSEUDONYMIZATION_PREDICTIVE_FILE = os.path.join(PSEUDONYMIZATION_FILES_FOLDER, "predictive.json")


def _generate_fake_OK_http_response(mocker, mock_json_value):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=mock_json_value)
    fake_resp.status_code = 200

    return fake_resp


def test_get_all_predictive_numbers_pseudonymize_sample_sheet(mocker, generate_list_of_pseudo_pred_numbers):
    mocker.patch("pseudonymization.pseudonymizers.old_miseq_pseudonymizer.PseudonymizePredictive.pseudonymize",
                 side_effect=generate_list_of_pseudo_pred_numbers)
    expected_predictive_numbers = ["102-20", "103-20", "104-20", "119-20", "125-20", "127-20",
                                   "137-20", "138-20", "139-20", "151-20", "152-20", "158-20", 
                                   "159-20", "160-20", "161-20", "162-20", "163-20", "171-20", "177-20"]
    expected_pred_pseudo_numbers = [(pred, pseudo) for (pred, pseudo)
                                    in zip(expected_predictive_numbers, generate_list_of_pseudo_pred_numbers)]

    predictive_pseudo_numbers = OldMiseqPseudonymizer(
        FAKE_RUN_FOR_TESTING,
        PSEUDONYMIZATION_FILES_FOLDER
    )._get_all_predictive_numbers_pseudonymize_sample_sheet()

    assert predictive_pseudo_numbers == expected_pred_pseudo_numbers


def test_rename_files_recursively():
    pseudonimizer = OldMiseqPseudonymizer(FAKE_RUN_FOR_TESTING, PSEUDONYMIZATION_FILES_FOLDER)

    pseudonimizer._pseudonymize_file_names_recursively("102-20", "000-00", FAKE_RUN_FOR_TESTING)

    assert os.path.exists(os.path.join(FAKE_RUN_FOR_TESTING,
                                       "Analysis",
                                       "000-00_Output",
                                       "000-00",
                                       "000-00_Parameters.txt"))


def test_rename_files_recursively_wrong_separator():
    pseudonimizer = OldMiseqPseudonymizer(FAKE_RUN_FOR_TESTING, PSEUDONYMIZATION_FILES_FOLDER)
    pseudonimizer._pseudonymize_file_names_recursively("152-20",
                                                       "000-00",
                                                       FAKE_RUN_FOR_TESTING)

    assert os.path.exists(os.path.join(FAKE_RUN_FOR_TESTING,
                                       "Analysis",
                                       "000-00_Output",
                                       "000-00",
                                       "000-00_Parameters.txt"))


def test_prepare_clinical_data_for_saving_non_empty(mocker,
                                                    generate_clinical_data_from_clinical_info_finder,
                                                    get_patient_psuedo_api_request,
                                                    get_sample_pseudo_api_request):
    
    fake_OK_patient_pseudo_response = _generate_fake_OK_http_response(mocker, get_patient_psuedo_api_request)
    fake_OK_sample_pseudo_response = _generate_fake_OK_http_response(mocker, get_sample_pseudo_api_request)

    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_sample.requests.get",
                  side_effect=[fake_OK_sample_pseudo_response, fake_OK_patient_pseudo_response])

    pseudonimizer = OldMiseqPseudonymizer(FAKE_RUN_FOR_TESTING, PSEUDONYMIZATION_FILES_FOLDER)
    random_pseudo_number = "mmci_predictive_12345678-1234-5678-1234-567812345621"
    clinical_data_dict = generate_clinical_data_from_clinical_info_finder

    data_for_saving = pseudonimizer._prepare_clinical_data_for_saving(clinical_data_dict, random_pseudo_number)

    assert isinstance(data_for_saving, Patient)
    assert data_for_saving.ID == "mmci_patient_12345678-1234-5678-1234-567812345621"

    assert isinstance(data_for_saving.samples, type([Material]))
    assert data_for_saving.samples[0].sample_ID == "mmci_sample_12345678-1234-5678-1234-567812345621"
    

def test_save_clinical_data(mocker, 
                            get_sample_pseudo_api_request, get_patient_psuedo_api_request,
                            get_tissue_dict_data, get_serum_dict_data):
    
    fake_OK_patient_pseudo_response = _generate_fake_OK_http_response(mocker, get_patient_psuedo_api_request)
    fake_OK_sample_pseudo_response = _generate_fake_OK_http_response(mocker, get_sample_pseudo_api_request)

    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_sample.requests.get",
                 side_effect=[fake_OK_sample_pseudo_response,
                              fake_OK_sample_pseudo_response,
                              fake_OK_patient_pseudo_response])
    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_sample.requests.get",
                 side_effect=[fake_OK_sample_pseudo_response,
                              fake_OK_sample_pseudo_response,
                              fake_OK_patient_pseudo_response])

    serum_predictive_pseudo_id = "mmci_predictive_12345678-1234-5678-1234-567812345688"
    tissue_predictive_psuedo_id = "mmci_predictive_12345678-1234-5678-1234-567812345689"

    samples = [
        Tissue(get_tissue_dict_data, tissue_predictive_psuedo_id, PSEUDONYMIZATION_PREDICTIVE_FILE),
        Serum(get_serum_dict_data, serum_predictive_pseudo_id, PSEUDONYMIZATION_PREDICTIVE_FILE)
    ]

    pat = Patient("mmci_patient_12345678-1234-5678-1234-567812345621", "Fri, 1 Mar 1990 00:00:00 GMT", 1, samples)

    folder_for_clinical_data = os.path.join(FAKE_RUN_FOR_TESTING, "catalog_info_per_pred_number")
    pseudo_pred_number = "mmci_patient_12345678-1234-5678-1234-567812345688"

    pseudonimizer = OldMiseqPseudonymizer(FAKE_RUN_FOR_TESTING, PSEUDONYMIZATION_FILES_FOLDER)
    pseudonimizer._save_clinical_data(pat, folder_for_clinical_data, pseudo_pred_number)

    assert os.path.exists(os.path.join(FAKE_RUN_FOR_TESTING,
                                       "catalog_info_per_pred_number",
                                       f"{pseudo_pred_number}.json"))


@pytest.fixture
def generate_list_of_pseudo_pred_numbers():
    return ["mmci_predictive_12345678-1234-5678-1234-5678123456" + "{:02d}".format(number) for number in range(0, 19)]


@pytest.fixture
def generate_clinical_data_from_clinical_info_finder():
    return {
        'ID': 111111,
        'birth_date': 'Sun, 01 Jan 1999 00:00:00 GMT',
        'consent': True,
        'sex': 1,
        'samples': [
            {'ID': 2006, 'available_samples_no': 3, 'biopsy_id': '2021/2244-1',
             'cut_time': 'Fri, 1 Mar 2021 00:00:00 GMT', 'diagnosis': 'C111',
             'freeze_time': 'Fri, 1 Mar 2021 11:45:00 GMT', 'material_type_id': '2',
             'morphology': '8720/39', 'patient_id': 111111, 'predictive_id': '2022/1111',
             'ptnm': 'TXN3M', 'retrieved': 'RetrievalType.operational',
             'sample_id': 'BBM:2021:111:2', 'samples_no': 3, 'type': 'Tissue'}
        ]
    }


@pytest.fixture
def get_patient_psuedo_api_request():
    return {
        "ID": 0,
        "patient_id": "111111",
        "patient_pseudo_ID": "mmci_patient_12345678-1234-5678-1234-567812345621",
    }


@pytest.fixture
def get_sample_pseudo_api_request():
    return {
        "id": 0,
        "sample_ID": "BBM:2021:111:2",
        "sample_pseudo_ID": "mmci_sample_12345678-1234-5678-1234-567812345621",
    }


@pytest.fixture
def get_serum_dict_data():
    serum_insides = {'ID': 2008, 'available_samples_no': 2, 'biopsy_id': '2021/2344-1',
                     'diagnosis': 'C110', 'material_type_id': '2',
                     'type': 'Serum', 'patient_id': 111112, 'predictive_id': '2020/1112',
                     'sample_id': 'BBM:2021:111:2', 'samples_no': 3, 'taking_date': "Fri, 1 Mar 2020 00:00:00 GMT"}
    return serum_insides


@pytest.fixture
def get_tissue_dict_data():
    tissue_insides = {'ID': 2008, 'available_samples_no': 2, 'biopsy_id': '2021/2344-1',
                      'cut_time': 'Fri, 5 Mar 2021 00:00:00 GMT', 'diagnosis': 'C110',
                      'freeze_time': 'Fri, 5 Mar 2021 11:45:00 GMT', 'material_type_id': '2',
                      'morphology': '8720/36', 'patient_id': 111112, 'predictive_id': '2020/1112',
                      'ptnm': 'TXN3M', 'retrieved': 'RetrievalType.operational',
                      'sample_id': 'BBM:2021:111:2', 'samples_no': 3, 'type': 'Tissue'}

    return tissue_insides


def _teardown_pseudonymization_files():
    shutil.rmtree(PSEUDONYMIZATION_FILES_FOLDER)


def _setup_pseudonymization_files():
    os.mkdir(PSEUDONYMIZATION_FILES_FOLDER)


def _copy_fake_run():
    shutil.copytree(FAKE_RUN_FOLDER_FOR_COPY, FAKE_RUN_FOR_TESTING)


def _remove_coppied_fake_run():
    shutil.rmtree(FAKE_RUN_FOR_TESTING)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_pseodonymization_files(request):
    _setup_pseudonymization_files()
    _copy_fake_run()

    request.addfinalizer(_teardown_pseudonymization_files)
    request.addfinalizer(_remove_coppied_fake_run)
