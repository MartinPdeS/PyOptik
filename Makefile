PYTHON ?= python3.11
BUILD_DIR ?= build
DIST_DIR ?= dist
DOCS_DIR ?= docs
DOCS_BUILD_DIR ?= $(DOCS_DIR)/build

.PHONY: help quality test docs build install uninstall quick rebuild editable \
	 setup download-all clean

help:
	@echo "PyOptik development targets:"
	@echo "  make quality       Run static checks"
	@echo "  make test          Run the offline test suite"
	@echo "  make docs          Build the documentation with warnings as errors"
	@echo "  make build         Build source and wheel distributions"
	@echo "  make install       Install the package"
	@echo "  make editable      Install the package in editable mode"
	@echo "  make setup         Download the complete material snapshot"
	@echo "  make download-all  Download the complete upstream catalog"
	@echo "  make quick         Run quality checks, tests, and build"
	@echo "  make rebuild       Clean, then run the quick workflow"
	@echo "  make clean         Remove generated build and test artifacts"

quality:
	$(PYTHON) -m flake8 PyOptik tests

test:
	MPLBACKEND=Agg MPLCONFIGDIR=$${TMPDIR:-/tmp}/pyoptik-matplotlib \
		$(PYTHON) -m pytest -m 'not network'

docs:
	MPLBACKEND=Agg MPLCONFIGDIR=$${TMPDIR:-/tmp}/pyoptik-matplotlib \
		$(PYTHON) -m sphinx -b html -W --keep-going \
			$(DOCS_DIR)/source $(DOCS_BUILD_DIR)/html

build:
	$(PYTHON) -m build --outdir $(DIST_DIR)

install:
	$(PYTHON) -m pip install .

uninstall:
	$(PYTHON) -m pip uninstall -y PyOptik

quick: quality test build

rebuild: clean quick

editable:
	$(PYTHON) -m pip install --no-build-isolation -e .

setup:
	$(PYTHON) -m PyOptik setup $(ARGS)

download-all:
	$(PYTHON) -m PyOptik download-all $(ARGS)

clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) $(DOCS_BUILD_DIR) \
		.pytest_cache htmlcov .coverage
