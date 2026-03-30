import pytest
import os


@pytest.fixture(autouse=True)
def mock_config_healthcheck(mocker, monkeypatch):
    monkeypatch.setenv("PSEUDONYMIZATION_API", "http://fake-api")
    monkeypatch.setenv("EXPORT_API", "http://fake-export-api")

    fake_resp = mocker.Mock()
    fake_resp.raise_for_status.return_value = None
    fake_resp.status_code = 200

    mocker.patch(
        "pseudonymization.config.config_processor.requests.get", return_value=fake_resp
    )
