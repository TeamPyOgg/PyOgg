import ctypes

from . import ogg
from . import opus
from .pyogg_error import PyOggError

class OpusFile:
    def __init__(self, path):
        # Open the file
        error = ctypes.c_int()
        of = opus.op_open_file(
            ogg.to_char_p(path),
            ctypes.pointer(error)
        )

        # Check for errors 
        if error.value != 0:
            raise PyOggError(
                "File couldn't be opened or doesn't exist. "+
                "Error code: {}".format(error.value)
            )

        # Extract the number of channels in the newly opened file
        #: Number of channels in audio file.
        self.channels = opus.op_channel_count(of, -1)

        # Allocate sufficient memory to store the entire PCM
        pcm_size = opus.op_pcm_total(of, -1)
        Buf = opus.opus_int16*(pcm_size*self.channels)
        buf = Buf()

        # Create a pointer to the newly allocated memory.  It
        # seems we can only do pointer arithmetic on void
        # pointers.  See
        # https://mattgwwalker.wordpress.com/2020/05/30/pointer-manipulation-in-python/
        buf_ptr = ctypes.cast(
            ctypes.pointer(buf),
            ctypes.c_void_p
        )
        buf_ptr_zero = buf_ptr.value

        #: Bytes per sample
        self.bytes_per_sample = ctypes.sizeof(opus.opus_int16)

        # Read through the entire file, copying the PCM into the
        # buffer
        samples = 0
        while True:
            # Calculate remaining buffer size
            remaining_buffer = (
                len(buf)
                - (buf_ptr.value
                   - buf_ptr_zero) // self.bytes_per_sample
            )

            # Convert buffer pointer to the desired type
            ptr = ctypes.cast(
                buf_ptr,
                ctypes.POINTER(opus.opus_int16)
            )

            # Read the next section of PCM
            ns = opus.op_read(
                of,
                ptr,
                remaining_buffer,
                ogg.c_int_p()
            )

            # Check for errors
            if ns<0:
                raise PyOggError(
                    "Error while reading OggOpus file. "+
                    "Error code: {}".format(ns)
                )

            # Increment the pointer
            buf_ptr.value += (
                ns
                * self.bytes_per_sample
                * self.channels
            )

            samples += ns

            # Check if we've finished
            if ns==0:
                break

        # Close the open file
        opus.op_free(of)

        # Opus files are always stored at 48k samples per second
        #: Number of samples per second (per channel).  Always 48,000.
        self.frequency = 48000

        # Store the buffer as Python bytes
        #: Raw PCM data from audio file.
        self.buffer = bytes(buf)

    def as_array(self):
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
