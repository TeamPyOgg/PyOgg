import shutil
from typing import Any

import pytest

from config import Config

        
_config = Config()


# FIXME: Mypy: What is the correct type for 'config'?  It is of type
# _pytest.config.Config (see
# https://docs.pytest.org/en/stable/_modules/_pytest/hookspec.html#pytest_configure)
# but this isn't part of the public API.  Using 'Any' as a
# placeholder.
def pytest_configure(config: Any) -> None:
    # Create an object to store the directories
    
    _config.rootdir = config.rootdir
    _config.outdir = config.rootdir / "tests/out"

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
    if _config.outdir.exists():
        _config.outdir.rename(config.rootdir / "tests/out_previous")

    # Create the output directory
    _config.outdir.mkdir()
    
    
@pytest.fixture(scope="session")
def pyogg_config() -> Config:
    return _config
