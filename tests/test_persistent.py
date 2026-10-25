import pytest
import subprocess
import persistent

def test_persistance():
    subprocess.run("python3 persistent.py -y", shell=True, text= True)
    result = subprocess.run("python3 dummy.py", shell=True, text= True, capture_output=True)
    assert result.stdout == "1\n"
    
    result = subprocess.run("python3 dummy.py", shell=True, text= True, capture_output=True)
    assert result.stdout == "2\n"
    
    subprocess.run("python3 persistent.py -y", shell=True, text= True)
 
def test_no_contamination():
    subprocess.run("python3 persistent.py -y", shell=True, text= True)
    
    subprocess.run("python3 dummy.py", shell=True, text= True)
    subprocess.run("python3 dummy.py", shell=True, text= True)
    subprocess.run("python3 dummy.py", shell=True, text= True)
    
    result = subprocess.run("python3 dummy2.py", shell=True, text= True, capture_output=True)
    assert result.stdout == "2\n"
    
    subprocess.run("python3 persistent.py -y", shell=True, text= True)