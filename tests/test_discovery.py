"""Source selection and compatibility checks for human-readable discovery."""

import importlib
from types import ModuleType

import numpy as np
import pytest
import yaml
from TypedUnit import ureg

from PyOptik import AmbiguousMaterialError, MaterialCatalog, find_materials, load_material, material


@pytest.fixture
def catalog(tmp_path):
    """A small offline catalog with competing datasets and source conditions."""
    families = {
        'main': {
            'Au': [('Johnson', 'Johnson and Christy 1972: n,k 0.4–0.8 µm'),
                   ('Johnson-film', 'Johnson thin film 1980: n,k 0.4–0.8 µm'),
                   ('Rakic-LD', 'Rakić et al. 1998: Lorentz-Drude model')],
            'SiO2': [('Malitson', 'Malitson 1965: fused silica'),
                     ('Ghosh', 'Ghosh 1999: quartz')],
            'H2O': [('Hale', 'Hale and Querry: water at 25 °C'),
                    ('Daimon-20.0C', 'Daimon and Masumura: water at 20 °C')],
            'Si': [('Test', 'Silicon')],
        },
        'specs': {
            'SCHOTT-optical': [('N-BK7', 'SCHOTT N-BK7')],
            'other-glass': [('N-BK7', 'Other manufacturer N-BK7')],
        },
    }
    shelves = []
    for shelf, books in families.items():
        book_nodes = []
        for book, pages in books.items():
            page_nodes = []
            for page, description in pages:
                relative = f'{shelf}/{book}/{page}.yml'
                path = tmp_path / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('REFERENCES: Synthetic test data\nDATA:\n'
                                '  - type: tabulated nk\n    data: |\n'
                                '      0.4 1.5 0.1\n      0.8 1.7 0.3\n')
                page_nodes.append({'PAGE': page, 'name': description, 'data': relative})
            book_nodes.append({'BOOK': book, 'content': page_nodes})
        shelves.append({'SHELF': shelf, 'content': book_nodes})
    catalog_file = tmp_path / 'catalog-nk.yml'
    catalog_file.write_text(yaml.safe_dump(shelves, allow_unicode=True))
    return MaterialCatalog(catalog_file, tmp_path)


@pytest.mark.parametrize('name,source,identifier', [
    ('Au', 'Johnson', 'main/Au/Johnson'),
    ('GOLD', 'johnson', 'main/Au/Johnson'),
    ('SiO2', 'Malitson', 'main/SiO2/Malitson'),
    ('fused silica', 'Malitson', 'main/SiO2/Malitson'),
    (' Fused-Silica ', 'Malitson', 'main/SiO2/Malitson'),
    ('water', 'Hale', 'main/H2O/Hale'),
    ('H2O', 'Daimon-20.0C', 'main/H2O/Daimon-20.0C'),
    ('BK7', None, 'specs/SCHOTT-optical/N-BK7'),
    ('N-BK7', None, 'specs/SCHOTT-optical/N-BK7'),
    ('silicon', None, 'main/Si/Test'),
    ('main/Au/Johnson', None, 'main/Au/Johnson'),
])
def test_common_names_load_explicit_dataset(catalog, name, source, identifier):
    result = material(name, source=source, catalog=catalog)
    assert result.catalog_id == identifier
    assert result.provenance['reference'] == 'Synthetic test data'
    assert result.provenance['source_url'].endswith(identifier + '.yml')
    assert result.nk(600 * ureg.nm) == pytest.approx(1.6 + 0.2j)


def test_ambiguity_lists_sources_and_preserves_candidates(catalog):
    with pytest.raises(AmbiguousMaterialError) as error:
        material('gold', catalog=catalog, use_default=False)
    message = str(error.value)
    assert 'Johnson and Christy 1972' in message
    assert '0.4–0.8 µm' in message
    assert "source='Johnson'" in message
    assert "material('main/Au/Johnson')" in message
    assert len(error.value.candidates) == 3


def test_cache_availability_does_not_choose_a_source(catalog):
    catalog.get('main/Au/Johnson-film').local_path.unlink()
    catalog.get('main/Au/Rakic-LD').local_path.unlink()
    with pytest.raises(AmbiguousMaterialError):
        material('Au', catalog=catalog, use_default=False)
    with pytest.raises(FileNotFoundError, match='pyoptik setup'):
        material('Au', source='Rakic-LD', catalog=catalog)


def test_source_matches_accents_and_descriptions(catalog):
    assert material('Au', source='Rakic et al.', catalog=catalog).catalog_id == 'main/Au/Rakic-LD'
    with pytest.raises(AmbiguousMaterialError):
        material('water', source='water', catalog=catalog)


def test_exact_book_does_not_match_other_chemical_formulas(catalog):
    assert [page.id.key for page in find_materials('Si', catalog=catalog)] == ['main/Si/Test']


def test_find_materials_returns_pages_without_loading(catalog):
    pages = find_materials('gold', catalog=catalog)
    assert len(pages) == 3
    assert pages[0].provenance()['id'] == 'main/Au/Johnson'
    assert find_materials('unknown', catalog=catalog) == []
    assert find_materials('main/Au/Missing', catalog=catalog) == []
    assert [page.id.page for page in find_materials('gold', source='Johnson', catalog=catalog)] == ['Johnson']
    assert material('Lorentz-Drude', catalog=catalog).catalog_id == 'main/Au/Rakic-LD'


def test_unknown_material_and_source_give_actionable_errors(catalog):
    with pytest.raises(KeyError, match="Did you mean 'gold'"):
        material('gld', catalog=catalog)
    with pytest.raises(KeyError, match='Available datasets: main/Au/Johnson'):
        material('gold', source='missing', catalog=catalog)
    with pytest.raises(KeyError, match='No material found'):
        material('main/Au/Missing', catalog=catalog)


@pytest.mark.parametrize('kwargs,error', [
    ({'name': ''}, ValueError),
    ({'name': '  -- '}, ValueError),
    ({'name': None}, TypeError),
    ({'name': 'Au', 'source': ''}, ValueError),
    ({'name': 'Au', 'source': 42}, TypeError),
    ({'name': 'Au', 'use_default': 'yes'}, TypeError),
])
def test_invalid_arguments_fail_before_any_download(monkeypatch, kwargs, error):
    def unexpected_download(**kwargs):
        raise AssertionError('Input validation must precede network access')
    monkeypatch.setattr(MaterialCatalog, 'from_snapshot', unexpected_download)
    with pytest.raises(error):
        material(**kwargs)


def test_cached_lookup_avoids_network_and_supports_data_root(catalog, monkeypatch):
    def unexpected_download(**kwargs):
        raise AssertionError('Cached lookup must not access the network')
    monkeypatch.setattr(MaterialCatalog, 'from_snapshot', unexpected_download)
    assert material('BK7', data_root=catalog.data_root).catalog_id == 'specs/SCHOTT-optical/N-BK7'
    with pytest.raises(ValueError, match='either catalog or data_root'):
        material('BK7', catalog=catalog, data_root=catalog.data_root)


def test_first_use_bootstraps_snapshot(catalog, tmp_path, monkeypatch):
    calls = []

    def snapshot(**kwargs):
        calls.append(kwargs)
        return catalog
    monkeypatch.setattr(MaterialCatalog, 'from_snapshot', snapshot)
    data_root = tmp_path / 'new-cache'
    assert material('BK7', data_root=data_root).catalog_id == 'specs/SCHOTT-optical/N-BK7'
    assert calls == [{'data_root': data_root}]


def test_material_package_remains_importable(catalog, monkeypatch):
    package = importlib.import_module('PyOptik.material')
    assert package is material
    assert isinstance(package, ModuleType)
    assert callable(package)
    from PyOptik.material import BaseMaterial, TabulatedMaterial
    assert isinstance(load_material('BK7', catalog=catalog), BaseMaterial)
    assert package.TabulatedMaterial is TabulatedMaterial
    monkeypatch.setattr('PyOptik.material.tabulated_class.material_paths', lambda kind: ())


def test_nk_accepts_arrays_and_validity_policy(catalog):
    gold = material('Au', source='Johnson', catalog=catalog, interpolation='pchip')
    wavelengths = [450, 650] * ureg.nm
    np.testing.assert_allclose(gold.nk(wavelengths), gold.refractive_index(wavelengths))
    assert gold.interpolation == 'pchip'
    with pytest.raises(ValueError):
        gold.nk(100 * ureg.nm, out_of_range='raise')


@pytest.mark.parametrize('name,identifier', [
    ('gold', 'main/Au/Johnson'),
    ('Au', 'main/Au/Johnson'),
    ('SiO2', 'main/SiO2/Malitson'),
    ('fused silica', 'main/SiO2/Malitson'),
    ('water', 'main/H2O/Hale'),
    ('H2O', 'main/H2O/Hale'),
])
def test_documented_defaults(catalog, name, identifier):
    assert material(name, catalog=catalog).catalog_id == identifier


def test_explicit_source_overrides_default(catalog):
    assert material('Au', source='Rakic-LD', catalog=catalog).catalog_id == 'main/Au/Rakic-LD'
    assert material('SiO2', source='Ghosh', catalog=catalog).catalog_id == 'main/SiO2/Ghosh'
    assert len(find_materials('Au', catalog=catalog)) == 3


def test_missing_default_never_falls_back_to_another_dataset(catalog):
    default = catalog.get('main/Au/Johnson')
    catalog._pages.pop(default.id)
    with pytest.raises(KeyError, match='Documented default.*absent'):
        material('Au', catalog=catalog)
    assert material('Au', source='Rakic-LD', catalog=catalog).catalog_id == 'main/Au/Rakic-LD'
    catalog._pages[default.id] = default
    default.local_path.unlink()
    with pytest.raises(FileNotFoundError, match='pyoptik setup'):
        material('Au', catalog=catalog)


def test_unrecognized_default_family_stays_ambiguous(catalog):
    with pytest.raises(AmbiguousMaterialError):
        material('water at', catalog=catalog)
