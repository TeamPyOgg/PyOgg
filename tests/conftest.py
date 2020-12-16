import shutil

import pytest

def pytest_configure(config):
    # Create an object to store the directories
    class Object:
        pass
    
    pyogg = Object()
    pyogg.rootdir = config.rootdir
    pyogg.outdir = config.rootdir / "tests/out"

    # Store the object in the pytest module
    pytest.pyogg = pyogg

    # If the previous output directory exists, delete it
    out_previous = config.rootdir / "tests/out_previous"
    if out_previous.exists():
        try:
            shutil.rmtree(out_previous)
        except Exception as e:
            raise Exception(
                "Failed to remove previous output directory.  "+
                "You will need to manually delete the directory "+
                f"'{out_previous}': "+str(e)
            )
    
    # If the output directory already exists, rename it
    if pyogg.outdir.exists():
        pyogg.outdir.rename(config.rootdir / "tests/out_previous")

    # Create the output directory
    pyogg.outdir.mkdir()
    
    
