"""Keep explicit release metadata consistent without Git version discovery."""

import re
import runpy
from importlib.metadata import version as distribution_version
from pathlib import Path

from packaging.version import Version
import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]


def test_explicit_release_metadata_agrees():
    """Source imports, distribution metadata, and Conda declare one version."""
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = metadata["project"]
    assert "version" not in project.get("dynamic", [])
    version_file = ROOT / metadata["tool"]["mps-maintenance"]["version-file"]
    package = runpy.run_path(str(version_file))
    assert package["__version__"] == package["version"] == project["version"]
    assert package["version_tuple"] == tuple(int(part) for part in project["version"].split("."))
    recipe = (ROOT / "conda.recipe/meta.yaml").read_text()
    assert re.search(r"^  version: (.+)$", recipe, re.MULTILINE)[1] == project["version"]
    assert metadata["tool"]["mps-maintenance"]["version-method"] == "literal"
    dependencies = metadata["build-system"]["requires"] + project["dependencies"]
    assert not any("setuptools-scm" in item.replace("_", "-") for item in dependencies)


def test_documentation_version_uses_package_version(monkeypatch):
    """Sphinx and its switcher use the package version instead of the tag environment."""
    pytest.importorskip("martinpdes_docs")
    if Version(distribution_version("MartinPdeS-docs")) < Version("0.4.0"):
        pytest.skip("automatic version discovery requires MartinPdeS-docs 0.4.0")
    monkeypatch.setenv("tag", "v9.9.9")
    config = runpy.run_path(str(ROOT / "docs" / "source" / "conf.py"))
    expected = runpy.run_path(str(ROOT / "PyOptik" / "_version.py"))["__version__"]
    assert config["version"] == config["release"] == expected
    assert config["html_theme_options"]["switcher"]["version_match"] == expected
