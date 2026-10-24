# Contributing to PyOptik

Contributions should preserve PyOptik's offline material-catalogue workflow.
Add tests for behaviour changes, document data provenance and physical units,
and avoid committing generated assets or caches. The release helper maintains
the tracked `PyOptik/_version.py` alongside `pyproject.toml` and the Conda recipe.

Use `make quality`, `make test`, and `make docs` as appropriate before a pull
request. Semantic release commands (`make release patch`, `minor`, or `major`)
create and push the release commit and exact tag; `make tag VERSION=vX.Y.Z`
creates a local-only tag.

## Shared release tooling

Install the pinned release tool in the interpreter used by Make, without
rebuilding this package:

```sh
python -m pip install "martinpdes-maintenance==0.2.1"
make release-check PYTHON=python
```

The same dependency is available through the project's `release` extra.
`tools/check_release.py`, `tools/next_release_version.py`, and
`tools/release_tag.py` are compatibility wrappers around `mps-maintenance`.
Package-specific metadata paths live in `[tool.mps-maintenance]` in
`pyproject.toml`. Release tooling is not a runtime dependency.

Preview the next release's metadata changes from a clean, full clone:

```sh
python tools/release_tag.py vX.Y.Z --dry-run
```

Fetch tags before selecting a version. Existing `make tag` and `make release`
commands keep their local-tag and push behavior respectively. The shared tool
requires an unused stable tag and a clean working tree. It stages only configured
release metadata and never pushes itself. If committing or tagging fails,
inspect `git status` and `git log -1` before recovering or retrying.

Package versions are explicit in `[project].version`. Builds do not derive
versions from Git tags or require setuptools-scm. Release commands update the
project version, package version file, and Conda recipe together.
