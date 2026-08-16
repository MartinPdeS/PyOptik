import ast
from pathlib import Path


def test_package_definitions_have_docstrings():
    """Ensure classes and methods remain documented as the API grows."""
    missing = []
    for path in Path("PyOptik").rglob("*.py"):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if ast.get_docstring(node) is None:
                missing.append(f"{path}:{node.lineno}:{node.name}")

    assert not missing, "Missing docstrings:\n" + "\n".join(missing)
