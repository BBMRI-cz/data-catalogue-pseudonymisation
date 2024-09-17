import os
import json
import pytest
from pseudonymization.models.Tissue import Tissue
from pseudonymization.models.Genome import Genome
from pseudonymization.models.Serum import Serum


@pytest.fixture
def tissues_specimen_api_mock():
    return {
        "ID": 2006, "available_samples_no": 3, "biopsy_id": "2021/2244-1",
        "cut_time": "Fri, 1 Mar 2021 00:00:00 GMT", "diagnosis": "C111",
        "freeze_time": "Fri, 1 Mar 2021 11:45:00 GMT", "material_type_id": "2",
        "morphology": "8720/39", "patient_id": 111111, "predictive_id": "2022/1111",
        "ptnm": "TXN3M", "retrieved": "RetrievalType.operational",
        "sample_id": "BBM:2021:111:2", "samples_no": 3, "type": "Tissue"
    }


@pytest.fixture
def genome_specimen_api_mock():
    return {
        "ID": 2006, "available_samples_no": 3, "biopsy_id": "2021/2244-1",
        "material_type_id": "2", "patient_id": 111111, "taking_date": "Fri, 1 Mar 2021 00:00:00 GMT",
        "predictive_id": "2022/1111", "retrieved": "RetrievalType.operational",
        "sample_id": "BBM:2021:111:2", "samples_no": 3, "type": "Genome"
    }


@pytest.fixture
def serum_specimen_api_mock():
    return {
        "ID": 2006, "available_samples_no": 3, "biopsy_id": "2021/2244-1", "diagnosis": "C111",
        "material_type_id": "K", "patient_id": 111111, "predictive_id": "2022/1111","sample_id": "BBM:2021:111:2",
        "samples_no": 3, "taking_date": "Fri, 1 Mar 2021 00:00:00 GMT", "type": "Serum"
    }


@pytest.fixture
def mock_get_sample_ok_return():
    return {
        "id": 1,
        "sample_ID": 2023-1112,
        "sample_pseudo_ID": "mmci_sample_12345678-1234-5678-1234-567812345678",
    }


def _remove_sample_table():
    os.remove("test_sample_table.json")


@pytest.fixture(autouse=True)
def create_pseudo_sample_table(request):
    with open("test_sample_table.json", "w") as f:
        json.dump({"samples": []}, f)

    request.addfinalizer(_remove_sample_table)


def _generate_fake_ok_http_response(mocker, mock_json_value):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=mock_json_value)
    fake_resp.status_code = 200

    return fake_resp


def test_tissue_correct_serialization(mocker, mock_get_sample_ok_return, tissues_specimen_api_mock):
    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_predictive.requests.get",
                 return_value=_generate_fake_ok_http_response(mocker, mock_get_sample_ok_return))

    tissue = Tissue(tissues_specimen_api_mock,
                    "mmci_predictive_12345678-1234-5678-1234-567812345678",
                    "test_sample_table.json")

    assert tissue.serialize() == {
            "pseudo_ID": "mmci_predictive_12345678-1234-5678-1234-567812345678",
            "biopsy_number": "2021/2244-1",
            "sample_ID": "mmci_sample_12345678-1234-5678-1234-567812345678",
            "sample_number": 3,
            "available_samples_number": 3,
            "material_type": "2",
            "material": "Tissue",
            "pTNM": "TXN3M",
            "morphology": "8720/39",
            "diagnosis": "C111",
            "cut_time": "01/03/2021, 00:00:00",
            "freeze_time": "01/03/2021, 11:45:00",
            "retrieved": "RetrievalType.operational",
    }


def test_genome_correct_serialization(mocker, mock_get_sample_ok_return, genome_specimen_api_mock):

    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_predictive.requests.get",
                 return_value=_generate_fake_ok_http_response(mocker, mock_get_sample_ok_return))

    genome = Genome(genome_specimen_api_mock,
                    "mmci_predictive_12345678-1234-5678-1234-567812345678",
                    "test_sample_table.json")

    assert genome.serialize() == {
        "pseudo_ID": "mmci_predictive_12345678-1234-5678-1234-567812345678",
        "biopsy_number": "2021/2244-1",
        "sample_ID": "mmci_sample_12345678-1234-5678-1234-567812345678",
        "sample_number": 3,
        "available_samples_number": 3,
        "material_type": "2",
        "material": "Genome",
        "retrieved": "RetrievalType.operational",
        "taking_date": "01/03/2021"
    }


def test_serum_correct_serialization(mocker, mock_get_sample_ok_return, serum_specimen_api_mock):
    mocker.patch("pseudonymization.pseudonimization_api.pseudonimize_predictive.requests.get",
                 return_value=_generate_fake_ok_http_response(mocker, mock_get_sample_ok_return))

    serum = Serum(serum_specimen_api_mock,
                  "mmci_predictive_12345678-1234-5678-1234-567812345678",
                  "test_sample_table.json")

    assert serum.serialize() == {
        "pseudo_ID": "mmci_predictive_12345678-1234-5678-1234-567812345678",
        "biopsy_number": "2021/2244-1",
        "sample_ID": "mmci_sample_12345678-1234-5678-1234-567812345678",
        "sample_number": 3,
        "available_samples_number": 3,
        "material_type": "K",
        "material": "Serum",
        "diagnosis": "C111",
        "taking_date": "01/03/2021"
    }
