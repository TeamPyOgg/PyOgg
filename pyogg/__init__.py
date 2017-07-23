__version__ = "0.0.1"
import ctypes
from . import ogg
from .ogg import PyOggError, PYOGG_OGG_AVAIL

if not PYOGG_OGG_AVAIL:
    raise PyOggError("libogg wasn't found or couldn't be loaded")

from . import vorbis
from.vorbis import PYOGG_VORBIS_AVAIL, PYOGG_VORBIS_FILE_AVAIL

from . import opus
from.opus import PYOGG_OPUS_AVAIL, PYOGG_OPUS_FILE_AVAIL

if not (PYOGG_OPUS_AVAIL and PYOGG_OPUS_FILE_AVAIL) and not (PYOGG_VORBIS_AVAIL and PYOGG_VORBIS_FILE_AVAIL):
    raise PyOggError("neither vorbis nor opus libraries were found")

class VorbisFile:
    def __init__(self, path):
        error, vf = vorbis.ov_fopen(path)
        info = vorbis.ov_info(vf, -1)

        self.channels = info.contents.channels

        self.frequency = info.contents.rate

        array = (ctypes.c_char*32768)()

        buffer_ = ctypes.cast(ctypes.pointer(array), ctypes.c_char_p)

        self.buffer = b""

        bitstream = ctypes.c_int()
        bitstream_pointer = ctypes.pointer(bitstream)

        while True:
            new_bytes = vorbis.ov_read(vf, buffer_, 32768, 0, 2, 1, bitstream_pointer)
            
            array_ = ctypes.cast(buffer_, ctypes.POINTER(ctypes.c_char*32768)).contents
            
            if self.buffer:
                self.buffer += array_.raw[:new_bytes]
            else:
                self.buffer = array_.raw[:new_bytes]

            del array_

            if new_bytes == 0:
                break

        del array

        del buffer_

        del bitstream

        del bitstream_pointer

        vorbis.ov_clear(vf)

        self.buffer_length = len(self.buffer)

class OpusFile:
    def __init__(self, path):
        error = ctypes.c_int()

        of = opus.op_open_file(ogg.to_char_p(path), ctypes.pointer(error))

        self.channels = opus.op_channel_count(of, -1)

        pcm_size = opus.op_pcm_total(of, -1)

        samples_read = ctypes.c_int(0)

        bfarr_t = opus.opus_int16*(pcm_size*self.channels)

        self.buffer = ctypes.cast(ctypes.pointer(bfarr_t()),opus.opus_int16_p)

        ptr = ctypes.cast(ctypes.pointer(self.buffer), ctypes.POINTER(ctypes.c_void_p))

        ptr_init = ptr.contents.value

        while samples_read.value < pcm_size:
            ptr.contents.value = ptr_init + samples_read.value*self.channels*2
            ns = opus.op_read(of, self.buffer , pcm_size*self.channels,ogg.c_int_p())
            samples_read.value += ns

        ptr.contents.value = ptr_init

        del ptr

        opus.op_free(of)

        self.buffer_length = samples_read.value*self.channels*2

        self.frequency = 48000
