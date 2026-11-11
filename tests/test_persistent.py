import pytest
import subprocess
import os
import sys
import shutil
from pathlib import Path

# run everything relative to the project root
ROOT = Path(__file__).resolve().parent.parent / 'tests' / 'resources'

def run(script, **kw):
    return subprocess.run([sys.executable, script], cwd=ROOT, text=True, **kw)

@pytest.fixture(autouse=True)
def reset_state():
    shutil.rmtree(ROOT / '.persistent', ignore_errors=True)

def test_persistance():
    result = run("dummy.py", capture_output=True)
    assert result.stdout == "1\n"

    result = run("dummy.py", capture_output=True)
    assert result.stdout == "2\n"
 
def test_no_contamination():
    run("dummy.py")
    run("dummy.py")
    run("dummy.py")
    
    result = run("dummy2.py", capture_output=True)
    assert result.stdout == "2\n"

def test_auto_init():
    for expected in ("1\n", "2\n"):
        result = run("dummy3.py", capture_output=True)
        assert result.stdout == expected

def test_auto_init_multiple_modules():
    # an imported module declaring first must not capture main's variables
    for expected in ("1 101 False\n", "2 102 False\n"):
        result = run("dummy4.py", capture_output=True)
        assert result.stdout == expected

def test_concurrent_access_no_corruption():
    # seed a valid value, then hammer it from many processes at once
    run("dummy5.py", capture_output=True)
    procs = [subprocess.Popen([sys.executable, "dummy5.py"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(30)]
    outputs = [p.communicate() for p in procs]
    for out, err in outputs:
        assert out == "OK\n", (out, err)
