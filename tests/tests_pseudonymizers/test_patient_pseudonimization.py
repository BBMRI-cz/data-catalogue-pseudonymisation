import pytest
from uuid import UUID
import os
import json

from pseudonymization.pseudonimization_api.pseudonimize_patient import (PseudonymizePatient)

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def mock_existing_patient():
    return {"ID":16,"patient_ID":123456,"patient_pseudo_ID":"mmci_patient_28237dcc-6c4b-4223-87e7-d99553f45a85"}


@pytest.fixture
def mock_non_existing_patient():
    return None


@pytest.fixture
def mock_POST_patient_OK_return():
    return {
        "data":{"patient_ID": "654321", "patient_pseudo_ID": "mmci_patient_12345678-1234-5678-1234-567812345678"},
        "isError": False,
        "message": "Success",
        "status_code": 200}


@pytest.fixture
def mock_new_uuid_value():
    return UUID('{12345678-1234-5678-1234-567812345678}')


def _setup_fake_patient_file():
    json_data = {
    "patients": [
        {
            "patient_ID": 123456,
            "patient_pseudo_ID": "mmci_patient_28237dcc-6c4b-4223-87e7-d99553f45a85"
        }
    ]}
    with open(os.path.join(CURRENT_DIRECTORY, "patients.json"), "w") as f:
        json.dump(json_data, f, indent=4)


def _teardown_fake_patient_file():
    os.remove(os.path.join(CURRENT_DIRECTORY, "patients.json"))


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_fake_patient_files(request):
    _setup_fake_patient_file()
    request.addfinalizer(_teardown_fake_patient_file)


def _generate_fake_OK_http_response(mocker, mock_json_value):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=mock_json_value)
    fake_resp.status_code = 200

    return fake_resp


def test_patient_exist(mocker, mock_existing_patient):
    fake_resp = _generate_fake_OK_http_response(mocker, mock_existing_patient)

    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_patient.requests.get", return_value=fake_resp)

    # Check if correct pseudo number was selected
    pat_pseudo = PseudonymizePatient("123456", os.path.join(CURRENT_DIRECTORY, "patients.json"))
    pseudo_predictive_number = pat_pseudo()

    assert pseudo_predictive_number == "mmci_patient_28237dcc-6c4b-4223-87e7-d99553f45a85"

    with open(os.path.join(CURRENT_DIRECTORY, "patients.json"), "r") as f:
        data = json.load(f)

    # Check if no new pseudo number was added to file (still size 1)
    assert len(data["patients"]) == 1

    for patient in data["patients"]:
        if patient["patient_ID"] == "123456":
            assert patient["patient_pseudo_ID"] == "mmci_patient_28237dcc-6c4b-4223-87e7-d99553f45a85"


def test_patient_not_exist(mocker, mock_non_existing_patient, mock_new_uuid_value, mock_POST_patient_OK_return):
    fake_GET_resp = _generate_fake_OK_http_response(mocker, mock_non_existing_patient)
    fake_POST_resp = _generate_fake_OK_http_response(mocker, mock_POST_patient_OK_return)

    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_patient.requests.get", return_value=fake_GET_resp)
    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_patient.requests.post", return_value=fake_POST_resp)
    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_patient.uuid.uuid4", return_value=mock_new_uuid_value)


    pat_pseudo = PseudonymizePatient("654321", os.path.join(CURRENT_DIRECTORY, "patients.json"))
    predictive_number = pat_pseudo()
    
    assert predictive_number == "mmci_patient_12345678-1234-5678-1234-567812345678"

    with open(os.path.join(CURRENT_DIRECTORY, "patients.json"), "r") as f:
        data = json.load(f)

    assert len(data["patients"]) == 2

    for patient in data["patients"]:
        if patient["patient_ID"] == "654321":
            assert patient["patient_pseudo_ID"] == "mmci_patient_12345678-1234-5678-1234-567812345678"