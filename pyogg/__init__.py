__version__ = "0.0.1"
from .ogg import *

if not PYOGG_OGG_AVAIL:
    raise PyOggError("libogg wasn't found or couldn't be loaded")

from .vorbis import *
from .opus import *

if not (PYOGG_OPUS_AVAIL and PYOGG_OPUS_FILE_AVAIL) and not (PYOGG_VORBIS_AVAIL and PYOGG_VORBIS_FILE_AVAIL):
    raise PyOggError("neither vorbis nor opus libraries were found")
