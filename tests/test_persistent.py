import pytest
import subprocess
import os
import sys
import shutil
from pathlib import Path

@pytest.fixture(autouse=True)
def reset_state():
    if Path('.persistent').exists():
        shutil.rmtree('.persistent')

def test_persistance():
    result = subprocess.run("python3 dummy.py", shell=True, text= True, capture_output=True)
    assert result.stdout == "1\n"
    
    result = subprocess.run("python3 dummy.py", shell=True, text= True, capture_output=True)
    assert result.stdout == "2\n"
    
    subprocess.run("python3 persistent.py -y", shell=True, text= True)
 
def test_no_contamination():
    subprocess.run("python3 dummy.py", shell=True, text= True)
    subprocess.run("python3 dummy.py", shell=True, text= True)
    subprocess.run("python3 dummy.py", shell=True, text= True)
    
    result = subprocess.run("python3 dummy2.py", shell=True, text= True, capture_output=True)
    assert result.stdout == "2\n"
    
    subprocess.run("python3 persistent.py -y", shell=True, text= True)

def test_auto_init():
    for expected in ("1\n", "2\n"):
        result = subprocess.run("python3 dummy3.py", shell=True, text=True, capture_output=True)
        assert result.stdout == expected

def test_auto_init_multiple_modules():
    # an imported module declaring first must not capture main's variables
    for expected in ("1 101 False\n", "2 102 False\n"):
        result = subprocess.run("python3 dummy4.py", shell=True, text=True, capture_output=True)
        assert result.stdout == expected
