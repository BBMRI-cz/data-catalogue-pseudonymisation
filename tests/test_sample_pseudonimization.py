import pytest
from uuid import UUID
import os
import json

from pseudonymization.pseudonimization_api.pseudonimize_sample import PseudonymizeSample

PSEUDONYMIZATION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples.json")


@pytest.fixture
def mock_existing_sample():
    return {"id":1,"sample_ID":"BBM:2021:111:1","sample_pseudo_ID":"mmci_sample_eefbaeee-8eee-4eee-beee-ee2ed600eeee"}

@pytest.fixture
def mock_non_existing_sample():
    return None

@pytest.fixture
def mock_new_uuid_value():
    return UUID('{12345678-1234-5678-1234-567812345678}')

def _setup_fake_sample_file():
    json_data ={
    "samples": [
        {
            "sample_ID": "BBM:2021:111:1",
            "pseudo_sample_ID": "mmci_sample_eefbaeee-8eee-4eee-beee-ee2ed600eeee"
        }
    ]}

    with open(PSEUDONYMIZATION_FILE, "w") as f:
        json.dump(json_data, f, indent=4)

def _teardown_fake_sample_file():
    os.remove(PSEUDONYMIZATION_FILE)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_fake_patient_files(request):
    _setup_fake_sample_file()
    request.addfinalizer(_teardown_fake_sample_file)

def _generate_fake_OK_http_response(mocker, mock_json_value):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=mock_json_value)
    fake_resp.status_code = 200

    return fake_resp


def test_predictive_exist(mocker, mock_existing_sample):
    fake_resp = _generate_fake_OK_http_response(mocker, mock_existing_sample)

    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_sample.requests.get", return_value=fake_resp)

    # Check if correct pseudo number was selected
    sample_pseudo = PseudonymizeSample("BBM:2021:111:1", PSEUDONYMIZATION_FILE)
    pseudo_sample_number = sample_pseudo()

    assert pseudo_sample_number == "mmci_sample_eefbaeee-8eee-4eee-beee-ee2ed600eeee"

    with open(PSEUDONYMIZATION_FILE, "r") as f:
        data = json.load(f)

    # Check if no new pseudo number was added to file (still size 1)
    assert len(data["samples"]) == 1

    for sample in data["samples"]:
        if sample["sample_ID"] == "BBM:2021:111:1":
            assert sample["pseudo_sample_ID"] == "mmci_sample_eefbaeee-8eee-4eee-beee-ee2ed600eeee"

def test_predictive_not_exist(mocker, mock_non_existing_sample, mock_new_uuid_value):
    fake_resp = _generate_fake_OK_http_response(mocker, mock_non_existing_sample)

    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_sample.requests.get", return_value=fake_resp)
    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_sample.uuid.uuid4", return_value=mock_new_uuid_value)
    sample_pseudo = PseudonymizeSample("BBM:2021:112:1", PSEUDONYMIZATION_FILE)
    sample_pseudo_number = sample_pseudo()
    
    assert sample_pseudo_number== "mmci_sample_12345678-1234-5678-1234-567812345678"

    with open(PSEUDONYMIZATION_FILE, "r") as f:
        data = json.load(f)

    assert len(data["samples"]) == 2

    for predictive in data["samples"]:
        if predictive["sample_ID"] == "BBM:2021:112:1":
            assert predictive["pseudo_sample_ID"] == "mmci_sample_12345678-1234-5678-1234-567812345678"