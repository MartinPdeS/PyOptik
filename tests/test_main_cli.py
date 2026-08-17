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
    assert 'command' in result.stdout
    assert '--verbose' in result.stdout
    assert 'download-all' in result.stdout
    assert 'setup' in result.stdout


def test_cli_download_all_dispatch(monkeypatch, tmp_path):
    """The complete-catalog command uses the bulk snapshot workflow."""
    module = importlib.import_module("PyOptik.__main__")
    calls = {}

    class FakeMaterialCatalog:
        @staticmethod
        def from_snapshot(data_root=None, force=False, progress=None):
            calls["from_snapshot"] = {
                "data_root": data_root,
                "force": force,
                "progress": progress,
            }
            return FakeMaterialCatalog

        @staticmethod
        def download_all(**kwargs):
            calls["download_all"] = kwargs

    monkeypatch.setattr(module, "MaterialCatalog", FakeMaterialCatalog)
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

    assert {
        key: value for key, value in calls["from_snapshot"].items() if key != "progress"
    } == {
        "data_root": tmp_path,
        "force": True,
    }
    assert callable(calls["from_snapshot"]["progress"])
    assert "download_all" not in calls


def test_cli_setup_uses_snapshot(monkeypatch, tmp_path):
    """The beginner setup command selects the bulk snapshot workflow."""
    module = importlib.import_module("PyOptik.__main__")
    calls = {}

    class FakeMaterialCatalog:
        @staticmethod
        def from_snapshot(**kwargs):
            calls["from_snapshot"] = kwargs
            return FakeMaterialCatalog

    monkeypatch.setattr(module, "MaterialCatalog", FakeMaterialCatalog)
    monkeypatch.setattr(
        sys,
        "argv",
        ["pyoptik", "setup", "--data-root", str(tmp_path), "--no-progress"],
    )

    module.main()

    assert calls["from_snapshot"] == {
        "data_root": tmp_path,
        "force": False,
        "progress": None,
    }
