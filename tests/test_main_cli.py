import subprocess
import sys
import importlib


def test_cli_help():
    result = subprocess.run(
        [sys.executable, '-m', 'PyOptik', '--help'],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert 'library' in result.stdout
    assert '--remove-previous' in result.stdout
    assert '--verbose' in result.stdout
    assert 'download-all' in result.stdout


def test_cli_list_libraries():
    result = subprocess.run(
        [sys.executable, '-m', 'PyOptik', '--list-libraries'],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert 'minimal' in result.stdout


def test_cli_download_all_dispatch(monkeypatch, tmp_path):
    """The complete-catalog command updates and then downloads the catalog."""
    module = importlib.import_module("PyOptik.__main__")
    calls = {}

    class FakeMaterialBank:
        @staticmethod
        def update_catalog(data_root=None):
            calls["data_root"] = data_root

        @staticmethod
        def download_all(**kwargs):
            calls["download_all"] = kwargs

    monkeypatch.setattr(module, "MaterialBank", FakeMaterialBank)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "pyoptik",
            "download-all",
            "--data-root",
            str(tmp_path),
            "--force",
            "--fail-fast",
        ],
    )

    module.main()

    assert calls["data_root"] == tmp_path
    assert calls["download_all"] == {"force": True, "continue_on_error": False}
