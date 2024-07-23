import pytest
import os
import sys
from pseudonymization.process.clinical_finder import ClinicalInfoFinder

TEST_RUN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_run")



@pytest.fixture
def empty_specimen_api_mock():
    return []

@pytest.fixture
def two_tissues_specimen_api_mock():
    return [
        {
            "ID":2006,"available_samples_no":3,"biopsy_id":"2021/2244-1",
            "cut_time":"Fri, 1 Mar 2021 00:00:00 GMT","diagnosis":"C111",
            "freeze_time":"Fri, 1 Mar 2021 11:45:00 GMT","material_type_id":"2",
            "morphology":"8720/39","patient_id":111111,"predictive_id":"2022/1111",
            "ptnm":"TXN3M","retrieved":"RetrievalType.operational",
            "sample_id":"BBM:2021:111:2","samples_no":3,"type":"Tissue"
        },
        {
            "ID":2007,"available_samples_no":1,"biopsy_id":"2021/2244-1",
            "cut_time":"Fri, 1 Mar 2021 00:00:00 GMT","diagnosis":"C111",
            "freeze_time":"Fri, 1 Mar 2021 11:45:00 GMT","material_type_id":"55",
            "morphology":"8720/39","patient_id":111111,"predictive_id":"2022/1111",
            "ptnm":"TXN3M","retrieved":"RetrievalType.operational",
            "sample_id":"BBM:2021:111:55","samples_no":1,"type":"Tissue"
        }]

@pytest.fixture
def no_patient_api_mock():
    return None

@pytest.fixture
def one_patient_api_mock():
    return {"ID":111111,"birth_date":"Sun, 01 Jan 1999 00:00:00 GMT","consent":True, "sex":1}

def _generate_fake_OK_http_response(mocker, mock_json_value):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=mock_json_value)
    fake_resp.status_code = 200

    return fake_resp

def _generate_fake_NOK_empty_http_response(mocker, mock_json_value):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=mock_json_value)
    fake_resp.status_code = 404

    return fake_resp


@pytest.mark.parametrize("original_pred_number, expected_fixed_pred_number", [("2022-1234", "2022-1234"),
                                                                              ("22-1234", "2022-1234"),
                                                                              ("1234-22", "2022-1234"),
                                                                              ("22_1234", "2022-1234"), 
                                                                              ("2022_1234", "2022-1234"),
                                                                              ("1950-1234", None)])
def test_pred_number_format_for_export(original_pred_number, expected_fixed_pred_number):
    fixed_pred_number = ClinicalInfoFinder(TEST_RUN_PATH)._fix_pred_number_format_for_export(original_pred_number)
    assert fixed_pred_number == expected_fixed_pred_number


def test_existing_pred_number_clinical_data_api(mocker, two_tissues_specimen_api_mock):
    fake_response = _generate_fake_OK_http_response(mocker, two_tissues_specimen_api_mock)
    mocker.patch("pseudonymization.process.clinical_finder.requests.get", return_value = fake_response)

    response = ClinicalInfoFinder(TEST_RUN_PATH)._get_clinical_data_from_pred_number("2022-1111")

    assert response[0]["predictive_id"] == "2022/1111"


def test_non_existing_pred_number_clinical_data_api(mocker, empty_specimen_api_mock):
    fake_response = _generate_fake_OK_http_response(mocker, empty_specimen_api_mock)
    mocker.patch("pseudonymization.process.clinical_finder.requests.get", return_value = fake_response)

    response = ClinicalInfoFinder(TEST_RUN_PATH)._get_clinical_data_from_pred_number("2022-0000")

    assert response == None


def test_existing_patient_number_clinical_data_api(mocker, two_tissues_specimen_api_mock, one_patient_api_mock):
    fake_response = _generate_fake_OK_http_response(mocker, one_patient_api_mock)
    mocker.patch("pseudonymization.process.clinical_finder.requests.get", return_value = fake_response)

    response = ClinicalInfoFinder(TEST_RUN_PATH)._get_patient_dict_based_on_sample_data(two_tissues_specimen_api_mock)

    assert response["ID"] == 111111

def test_non_existing_patient_number_clinical_data_api(mocker, no_patient_api_mock, two_tissues_specimen_api_mock):
    fake_response = _generate_fake_NOK_empty_http_response(mocker, no_patient_api_mock)
    mocker.patch("pseudonymization.process.clinical_finder.requests.get", return_value = fake_response)

    response = ClinicalInfoFinder(TEST_RUN_PATH)._get_patient_dict_based_on_sample_data(two_tissues_specimen_api_mock)

    assert response == None


def test_non_empty_collect_clinical_data_based_on_pred_number_better(mocker, two_tissues_specimen_api_mock, one_patient_api_mock):
    fake_response_samples = _generate_fake_OK_http_response(mocker, two_tissues_specimen_api_mock)
    fake_response_patient = _generate_fake_OK_http_response(mocker, one_patient_api_mock)
    mocker.patch("pseudonymization.process.clinical_finder.requests.get", side_effect=[fake_response_samples, fake_response_patient])

    response = ClinicalInfoFinder(TEST_RUN_PATH).collect_clinical_data("2022-1111")

    assert response["ID"] == 111111
    sample_ids = [sample["sample_id"] for sample in response["samples"]]
    assert sample_ids == ["BBM:2021:111:2", "BBM:2021:111:55"]

def test_empty_collect_clinical_data_based_on_pred_number(mocker, empty_specimen_api_mock):
    fake_response_no_specimen = _generate_fake_NOK_empty_http_response(mocker, empty_specimen_api_mock)
    mocker.patch("pseudonymization.process.clinical_finder.requests.get", return_value=fake_response_no_specimen)
    
    response = ClinicalInfoFinder(TEST_RUN_PATH).collect_clinical_data("2022-0000")
    assert response == None