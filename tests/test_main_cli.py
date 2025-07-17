import subprocess
import sys


def test_cli_help():
    result = subprocess.run(
        [sys.executable, '-m', 'PyOptik', '--help'],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert 'library' in result.stdout
    assert '--remove-previous' in result.stdout


def test_cli_list_libraries():
    result = subprocess.run(
        [sys.executable, '-m', 'PyOptik', '--list-libraries'],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert 'minimal' in result.stdout

