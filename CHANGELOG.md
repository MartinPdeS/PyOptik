# Changelog

All notable changes to PyOptik are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for all nine RefractiveIndex.INFO dispersion formula types.
- `MaterialCatalog.search()` with hierarchy, source, reference, and local
  availability filters.
- `MaterialPage.provenance()` for serializable material-source records.
- `MaterialCatalog.verify_integrity()` for SHA-256 verification of cached
  material data.
- `compute_group_delay_wavelength_slope()` for the explicit wavelength-space
  derivative, `dτ_g/dλ`.
- Numerical regression, unit-equivalence, catalog-search, and cache-integrity
  test coverage.
- A new PyOptik prism logo and documentation favicon.

### Changed

- `compute_group_delay_dispersion()` now returns conventional frequency-domain
  GDD, `dτ_g/dω`, with time-squared units.
- Material plots use a consistent built-in Matplotlib layout and typography.
- Public catalog and group-delay APIs use expanded NumPy-style docstrings.

### Fixed

- Formula type 6 now accumulates every gas-dispersion term instead of
  overwriting earlier terms.

### Removed

- The `MPSPlots` runtime dependency and its use in examples and material
  plotting helpers.
- Retired logo assets.

[Unreleased]: https://github.com/MartinPdeS/PyOptik/compare/v3.0.0...HEAD
