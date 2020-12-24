import pathlib

# Definition of class returned by PyTest fixture 'pyogg_config'.
class Config:
    def __init__(self):
        self.rootdir: pathlib.Path
        self.outdir: pathlib.Path
