# Changelog

All notable changes to PyOptik are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.2.0] - 2026-09-16

### Added

- Task-oriented getting-started and material-catalog guides.
- Executable gallery examples for measured-material import and YAML round
  trips, Fresnel polarization and Brewster angle, quarter-wave antireflection
  coatings, dielectric Bragg mirrors, and catalog provenance workflows.
- Direct README links to the principal guides, examples, and API reference.

### Changed

- Documentation navigation now groups content into Start here, User guide,
  Learn by example, and Reference sections.
- The documentation landing page, page titles, API hierarchy, and gallery
  descriptions now use clearer task-oriented language.

## [3.1.0] - 2026-09-16

### Added

- Support for all nine RefractiveIndex.INFO dispersion formula types.
- `MaterialCatalog.search()` with hierarchy, source, reference, and local
  availability filters.
- `MaterialPage.provenance()` for serializable material-source records.
- `MaterialCatalog.verify_integrity()` for SHA-256 verification of cached
  material data.
- `compute_group_delay_wavelength_slope()` for the explicit wavelength-space
  derivative, `dτ_g/dλ`.
- Convenience APIs for real index, extinction coefficient, relative
  permittivity, and absorption coefficient.
- Split tabulated ``n`` and ``k`` YAML support and opt-in monotonic PCHIP
  interpolation.
- A physical conventions and provenance documentation guide.
- Numerical regression, unit-equivalence, catalog-search, and cache-integrity
  test coverage.
- A new PyOptik prism logo and documentation favicon.
- Typed, validated material documents for formula and tabulated optical data.
- User-defined material construction from arrays, CSV files, and formula
  coefficients, with atomic RefractiveIndex.INFO-compatible YAML export.
- An optional Textual terminal browser for searching the local material
  catalog and inspecting provenance.
- Fresnel reflection and transmission calculations for s and p polarization,
  including Brewster and critical-angle helpers.
- Coherent transfer-matrix calculations for isotropic multilayer thin films,
  supporting constant complex indices and wavelength-dependent PyOptik
  material models.
- Numerical reference tests for interfaces, total internal reflection,
  antireflection coatings, absorbing films, custom material round trips, and
  malformed input paths.

### Changed

- `compute_group_delay_dispersion()` now returns conventional frequency-domain
  GDD, `dτ_g/dω`, with time-squared units.
- Material plots use a consistent built-in Matplotlib layout and typography.
- Public catalog and group-delay APIs use expanded NumPy-style docstrings.
- Material YAML loading and export share one typed parser and validation layer.
- Wavelength validity endpoints tolerate floating-point round-off introduced
  by unit conversions.

### Fixed

- Formula type 6 now accumulates every gas-dispersion term instead of
  overwriting earlier terms.

### Removed

- The `MPSPlots` runtime dependency and its use in examples and material
  plotting helpers.
- Retired logo assets.

[Unreleased]: https://github.com/MartinPdeS/PyOptik/compare/v3.2.0...HEAD
[3.2.0]: https://github.com/MartinPdeS/PyOptik/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/MartinPdeS/PyOptik/compare/v3.0.5...v3.1.0
