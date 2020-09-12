import ctypes

from . import vorbis
from .pyogg_error import PyOggError

class VorbisFile:
    def __init__(self, path):
        # TODO: This method looks to be in need of a clean up.
        # Compare with OpusFile.__init__().
        
        vf = vorbis.OggVorbis_File()
        error = vorbis.libvorbisfile.ov_fopen(vorbis.to_char_p(path), ctypes.byref(vf))
        if error != 0:
            raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error))

        info = vorbis.libvorbisfile.ov_info(ctypes.byref(vf), -1)

        #: Number of channels in audio file.
        self.channels = info.contents.channels

        #: Number of samples per second (per channel), 44100 for
        #  example.
        self.frequency = info.contents.rate

        array = (ctypes.c_char*4096)()

        buffer_ = ctypes.cast(ctypes.pointer(array), ctypes.c_char_p)

        self.buffer_array = []

        bitstream = ctypes.c_int()
        bitstream_pointer = ctypes.pointer(bitstream)

        while True:
            new_bytes = vorbis.libvorbisfile.ov_read(ctypes.byref(vf), buffer_, 4096, 0, 2, 1, bitstream_pointer)

            array_ = ctypes.cast(buffer_, ctypes.POINTER(ctypes.c_char*4096)).contents

            self.buffer_array.append(array_.raw[:new_bytes])

            if new_bytes == 0:
                break

        #: Raw PCM data from audio file.
        self.buffer = b"".join(self.buffer_array)

        vorbis.libvorbisfile.ov_clear(ctypes.byref(vf))

        #: Length of the buffer
        self.buffer_length = len(self.buffer)

        #: Bytes per sample
        self.bytes_per_sample = 2 # TODO: Where is this actually defined?

    def as_array(self):
        # TODO: This method is identical to that of
        # OpusFile.as_array().  Perhaps it would be better to form a
        # common base class?
        
        """Returns the buffer as a NumPy array.

        The shape of the returned array is in units of (number of
        samples per channel, number of channels).

        The data type is 16-bit signed integers.

        The buffer is not copied, but rather the NumPy array
        shares the memory with the buffer.

        """

        import numpy

        # Convert the bytes buffer to a NumPy array
        array = numpy.frombuffer(
            self.buffer,
            dtype=numpy.int16
        )

        # Reshape the array
        return array.reshape(
            (len(self.buffer)
             // self.bytes_per_sample
             // self.channels,
             self.channels)
        )
