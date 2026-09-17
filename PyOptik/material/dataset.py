"""Typed, validated representations of PyOptik material datasets."""


from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy
import yaml


@dataclass(frozen=True)
class MaterialMetadata:
    """Source metadata shared by formula and tabulated datasets."""

    reference: str | None = None
    conditions: Mapping[str, Any] = field(default_factory=dict)
    comments: str | None = None


@dataclass(frozen=True)
class FormulaDataset:
    """A validated RefractiveIndex.INFO formula dataset."""

    formula_type: int
    coefficients: tuple[float, ...]
    wavelength_range: tuple[float, float] | None = None

    def __post_init__(self) -> None:
        """Validate formula identity, coefficients, and optional bounds."""
        if self.formula_type not in range(1, 10):
            raise ValueError(f"Unsupported formula type: {self.formula_type}")
        if not self.coefficients or not numpy.all(numpy.isfinite(self.coefficients)):
            raise ValueError("formula coefficients must be a non-empty finite sequence")
        _validate_range(self.wavelength_range)


@dataclass(frozen=True)
class TabulatedDataset:
    """One validated table of ``n``, ``k``, or combined ``nk`` values."""

    kind: str
    wavelength_um: tuple[float, ...]
    values: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        """Validate shape, finiteness, and wavelength ordering."""
        if self.kind not in {"n", "k", "nk"}:
            raise ValueError("tabulated kind must be 'n', 'k', or 'nk'")
        expected = 2 if self.kind == "nk" else 1
        if len(self.wavelength_um) < 2 or len(self.values) != len(self.wavelength_um):
            raise ValueError(f"tabulated {self.kind} data must contain at least two rows")
        if any(len(row) != expected for row in self.values):
            raise ValueError(f"tabulated {self.kind} rows require {expected + 1} columns")
        wavelength = numpy.asarray(self.wavelength_um, dtype=float)
        data = numpy.asarray(self.values, dtype=float)
        if not numpy.all(numpy.isfinite(wavelength)) or not numpy.all(numpy.isfinite(data)):
            raise ValueError("tabulated data must be finite")
        if numpy.any(numpy.diff(wavelength) <= 0):
            raise ValueError("tabulated wavelengths must be strictly increasing")


Dataset = FormulaDataset | TabulatedDataset


@dataclass(frozen=True)
class MaterialDocument:
    """A parsed optical-material document and its provenance metadata."""

    datasets: tuple[Dataset, ...]
    metadata: MaterialMetadata = field(default_factory=MaterialMetadata)

    def __post_init__(self) -> None:
        """Require at least one supported dataset."""
        if not self.datasets:
            raise ValueError("material document contains no supported dataset")

    @property
    def formula_datasets(self) -> tuple[FormulaDataset, ...]:
        """Return formula datasets in source order."""
        return tuple(item for item in self.datasets if isinstance(item, FormulaDataset))

    @property
    def tabulated_datasets(self) -> tuple[TabulatedDataset, ...]:
        """Return tabulated datasets in source order."""
        return tuple(item for item in self.datasets if isinstance(item, TabulatedDataset))

    def to_mapping(self) -> dict[str, Any]:
        """Return a RefractiveIndex.INFO-compatible YAML mapping."""
        document: dict[str, Any] = {}
        if self.metadata.reference is not None:
            document["REFERENCES"] = self.metadata.reference
        if self.metadata.comments is not None:
            document["COMMENTS"] = self.metadata.comments
        if self.metadata.conditions:
            document["CONDITIONS"] = dict(self.metadata.conditions)
        entries = []
        for dataset in self.datasets:
            if isinstance(dataset, FormulaDataset):
                entry: dict[str, Any] = {
                    "type": f"formula {dataset.formula_type}",
                    "coefficients": " ".join(_format_number(value) for value in dataset.coefficients),
                }
                if dataset.wavelength_range is not None:
                    entry["wavelength_range"] = " ".join(
                        _format_number(value) for value in dataset.wavelength_range
                    )
            else:
                rows = []
                for wavelength, values in zip(dataset.wavelength_um, dataset.values):
                    rows.append(" ".join(_format_number(value) for value in (wavelength, *values)))
                entry = {"type": f"tabulated {dataset.kind}", "data": "\n".join(rows) + "\n"}
            entries.append(entry)
        document["DATA"] = entries
        return document

    def to_yaml(self, path: str | Path) -> Path:
        """Serialize this document to ``path`` and return the resulting path."""
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8") as stream:
            yaml.safe_dump(self.to_mapping(), stream, sort_keys=False, allow_unicode=True)
        temporary.replace(destination)
        return destination


def parse_material(source: str | Path | Mapping[str, Any]) -> MaterialDocument:
    """Parse and validate a material YAML path or already-loaded mapping."""
    if isinstance(source, Mapping):
        raw = dict(source)
        label = "material mapping"
    else:
        path = Path(source)
        label = str(path)
        try:
            with path.open("r", encoding="utf-8") as stream:
                raw = yaml.safe_load(stream)
        except (OSError, yaml.YAMLError) as error:
            raise ValueError(f"Unable to read material YAML {label}: {error}") from error
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid material YAML in {label}: expected a mapping")
    entries = raw.get("DATA")
    if not isinstance(entries, list):
        raise ValueError(f"Invalid material YAML in {label}: DATA must be a list")
    datasets: list[Dataset] = []
    try:
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError("DATA entries must be mappings")
            tokens = str(entry.get("type", "")).lower().split()
            if len(tokens) != 2:
                continue
            if tokens[0] == "formula":
                wavelength_range = (
                    _numbers(entry["wavelength_range"])
                    if "wavelength_range" in entry else ()
                )
                datasets.append(FormulaDataset(
                    formula_type=int(tokens[1]),
                    coefficients=_numbers(entry["coefficients"]),
                    wavelength_range=tuple(wavelength_range) if wavelength_range else None,
                ))
            elif tokens[0] == "tabulated" and tokens[1] in {"n", "k", "nk"}:
                rows = tuple(_numbers(line) for line in str(entry["data"]).strip().splitlines())
                datasets.append(TabulatedDataset(
                    kind=tokens[1],
                    wavelength_um=tuple(row[0] for row in rows),
                    values=tuple(tuple(row[1:]) for row in rows),
                ))
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"Invalid material dataset in {label}: {error}") from error
    try:
        metadata = MaterialMetadata(
            reference=str(raw["REFERENCES"]) if raw.get("REFERENCES") is not None else None,
            conditions=dict(raw.get("CONDITIONS") or {}),
            comments=str(raw["COMMENTS"]) if raw.get("COMMENTS") is not None else None,
        )
    except (TypeError, ValueError) as error:
        raise ValueError(f"Invalid material metadata in {label}: {error}") from error
    try:
        return MaterialDocument(tuple(datasets), metadata)
    except ValueError as error:
        raise ValueError(f"Invalid material dataset in {label}: {error}") from error


def _numbers(value: str | Sequence[float]) -> tuple[float, ...]:
    """Convert whitespace-delimited text or a sequence to floats."""
    values = value.split() if isinstance(value, str) else value
    return tuple(float(item) for item in values)


def _validate_range(value: tuple[float, float] | None) -> None:
    """Validate an optional increasing two-value wavelength interval."""
    if value is None:
        return
    if len(value) != 2 or not numpy.all(numpy.isfinite(value)) or value[0] >= value[1]:
        raise ValueError("wavelength_range must contain two increasing finite values")


def _format_number(value: float) -> str:
    """Format a float precisely enough for lossless YAML round trips."""
    return format(float(value), ".17g")
