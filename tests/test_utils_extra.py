from pathlib import Path
from unittest.mock import Mock
import pytest
import requests

from PyOptik.utils import download_yml_file
from PyOptik.material_type import MaterialType


class DummyResponse:
    def __init__(self, status_code=200, content=b"ok"):
        self.status_code = status_code
        self.content = content

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"status {self.status_code}")

def test_download_success(monkeypatch, tmp_path):
    monkeypatch.setattr('PyOptik.utils.sellmeier_data_path', tmp_path)
    resp = DummyResponse()
    monkeypatch.setattr(requests, 'get', lambda *a, **k: resp)
    download_yml_file('http://foo', 'file', MaterialType.SELLMEIER)
    assert (tmp_path / 'file.yml').read_bytes() == resp.content


def test_download_http_error(monkeypatch, tmp_path):
    monkeypatch.setattr('PyOptik.utils.sellmeier_data_path', tmp_path)
    resp = DummyResponse(status_code=404)
    monkeypatch.setattr(requests, 'get', lambda *a, **k: resp)
    with pytest.raises(requests.exceptions.HTTPError):
        download_yml_file('http://foo', 'file', MaterialType.SELLMEIER)


def test_download_timeout(monkeypatch):
    monkeypatch.setattr(requests, 'get', Mock(side_effect=requests.exceptions.Timeout))
    with pytest.raises(requests.exceptions.Timeout):
        download_yml_file('http://foo', 'file', MaterialType.SELLMEIER)

if __name__ == "__main__":
    pytest.main(["-W error", "-s", __file__])
