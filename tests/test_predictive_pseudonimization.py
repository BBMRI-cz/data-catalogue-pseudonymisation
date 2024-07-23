import pytest
from uuid import UUID
import os
import json

from pseudonymization.pseudonimization_api.pseudonimize_predictive import PseudonymizePredictive

PSEUDONYMIZATION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "predictive.json")


@pytest.fixture
def mock_existing_predictive():
    return {"predictive_ID": "2023-1111", "predictive_ID_unified":"1111-23", "predictive_pseudo_ID":"mmci_predictive_11f6afb1-9f11-4cee-ee47-eee5f5a8e0ee"}

@pytest.fixture
def mock_non_existing_predictive():
    return None

@pytest.fixture
def mock_new_uuid_value():
    return UUID('{12345678-1234-5678-1234-567812345678}')

@pytest.fixture
def mock_POST_predictive_OK_return():
    return {
        "data": {
            "predictive_ID": "2023-1112",
            "predictive_pseudo_ID": "mmci_predictive_99597ef6-6a6d-4223-b24f-7cde65d82bcf"
        },
        "isError": False,
        "message": "Success",
        "statusCode": 200
    }

def _setup_fake_predictive_file():
    json_data = {
    "predictive": [
        {
            "predictive_number": "2023-1111",
            "pseudo_number": "mmci_predictive_11f6afb1-9f11-4cee-ee47-eee5f5a8e0ee"
        }
    ]}
    with open(PSEUDONYMIZATION_FILE, "w") as f:
        json.dump(json_data, f, indent=4)

def _teardown_fake_predictive_file():
    os.remove(PSEUDONYMIZATION_FILE)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_fake_patient_files(request):
    _setup_fake_predictive_file()
    request.addfinalizer(_teardown_fake_predictive_file)

def _generate_fake_OK_http_response(mocker, mock_json_value):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=mock_json_value)
    fake_resp.status_code = 200

    return fake_resp

def test_predictive_exist(mocker, mock_existing_predictive):
    fake_resp = _generate_fake_OK_http_response(mocker, mock_existing_predictive)

    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_predictive.requests.get", return_value=fake_resp)

    # Check if correct pseudo number was selected
    pat_pseudo = PseudonymizePredictive(PSEUDONYMIZATION_FILE)
    pseudo_predictive_number = pat_pseudo.pseudonimize("2023-1111")

    assert pseudo_predictive_number == "mmci_predictive_11f6afb1-9f11-4cee-ee47-eee5f5a8e0ee"

    with open(PSEUDONYMIZATION_FILE, "r") as f:
        data = json.load(f)

    # Check if no new pseudo number was added to file (still size 1)
    assert len(data["predictive"]) == 1

    for predictive in data["predictive"]:
        if predictive["predictive_number"] == "2023-1111":
            assert predictive["pseudo_number"] == "mmci_predictive_11f6afb1-9f11-4cee-ee47-eee5f5a8e0ee"

def test_predictive_not_exist(mocker, mock_non_existing_predictive, mock_new_uuid_value, mock_POST_predictive_OK_return):
    fake_GET_resp = _generate_fake_OK_http_response(mocker, mock_non_existing_predictive)
    fake_POST_resp = _generate_fake_OK_http_response(mocker, mock_POST_predictive_OK_return)
 
    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_predictive.requests.get", return_value=fake_GET_resp)
    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_predictive.requests.post", return_value=fake_POST_resp)
    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_predictive.uuid.uuid4", return_value=mock_new_uuid_value)
    
    pat_pseudo = PseudonymizePredictive(PSEUDONYMIZATION_FILE)
    predictive_number = pat_pseudo.pseudonimize("2023-1112")
    
    assert predictive_number == "mmci_predictive_12345678-1234-5678-1234-567812345678"

    with open(PSEUDONYMIZATION_FILE, "r") as f:
        data = json.load(f)

    assert len(data["predictive"]) == 2

    for predictive in data["predictive"]:
        if predictive["predictive_number"] == "2023-1112":
            assert predictive["pseudo_number"] == "mmci_predictive_12345678-1234-5678-1234-567812345678"