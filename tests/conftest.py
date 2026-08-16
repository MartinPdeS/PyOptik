"""Shared test configuration."""

import os
from pathlib import Path

import matplotlib

os.environ.setdefault("PYOPTIK_DATA_DIR", "/tmp/pyoptik-test-data")
matplotlib.use("Agg")

# Redirect all already-imported path aliases as well as the environment-based
# configuration. Tests must never write into a developer's package data dir.
import PyOptik.directories as directories

test_data_path = Path(os.environ["PYOPTIK_DATA_DIR"])
directories.user_data_path = test_data_path
directories.user_sellmeier_data_path = test_data_path / "sellmeier"
directories.user_tabulated_data_path = test_data_path / "tabulated"

import PyOptik.material_bank as material_bank
import PyOptik.utils as utils

material_bank.user_data_path = test_data_path
utils.sellmeier_data_path = directories.user_sellmeier_data_path
utils.tabulated_data_path = directories.user_tabulated_data_path
