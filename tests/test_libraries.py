import pyogg

def test_ogg():
    assert pyogg.PYOGG_OGG_AVAIL

def test_opus():
    assert pyogg.PYOGG_OPUS_AVAIL

def test_opus_file():
    assert pyogg.PYOGG_OPUS_FILE_AVAIL

# Can't find library for Ubuntu Xenial (Travis CI)
#def test_opus_enc():
#    assert pyogg.PYOGG_OPUS_ENC_AVAIL
    
def test_vorbis():
    assert pyogg.PYOGG_VORBIS_AVAIL

def test_vorbis_file():
    assert pyogg.PYOGG_VORBIS_FILE_AVAIL

def test_vorbis_enc():
    assert pyogg.PYOGG_VORBIS_ENC_AVAIL

def test_flac():
    assert pyogg.PYOGG_FLAC_AVAIL
