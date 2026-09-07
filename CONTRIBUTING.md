# Contributing to PyOptik

Contributions should preserve PyOptik's offline material-catalogue workflow.
Add tests for behaviour changes, document data provenance and physical units,
and avoid committing generated assets, caches, or `PyOptik/_version.py`.

Use `make quality`, `make test`, and `make docs` as appropriate before a pull
request. Semantic release commands (`make release patch`, `minor`, or `major`)
create and push the release commit and exact tag; `make tag VERSION=vX.Y.Z`
creates a local-only tag.
