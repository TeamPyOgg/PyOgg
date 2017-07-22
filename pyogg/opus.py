import ctypes
import ctypes.util

try:
    libopus = ctypes.CDLL("libopus.dll")
    libopusfile = ctypes.CDLL("libopusfile.dll")
except:
    libopus = None
    libopusfile = None

if not libopus:
    PYOGG_OPUS_AVAIL = False
else:
    PYOGG_OPUS_AVAIL = True
    
if not libopusfile:
    PYOGG_OPUS_FILE_AVAIL = False
else:
    PYOGG_OPUS_FILE_AVAIL = True

