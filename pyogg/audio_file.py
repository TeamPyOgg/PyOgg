import ctypes
from typing import Any

from .pyogg_error import PyOggError

class AudioFile:
    """Abstract base class for audio files.

    This class is a base class for audio files (such as Vorbis, Opus,
    and FLAC).  It should not be instatiated directly.

    It is assumed that the audio data is stored in either 8-bit or
    16-bit integer samples.

    """
    def __init__(self) -> None:
        """AudioFile should not be directly instantiated."""
        #: Number of channels in audio file.
        self.channels: int

        #: Raw bytes of audio data.  Channels are interleaved.
        self.buffer: ctypes.Array

        #: Bytes per sample.  For example, CD-quality audio has 16-bit
        #: samples (2 bytes per sample).  Floating-point
        #: representations are not supported.
        self.bytes_per_sample: int

        #: Signedness of the samples.  True if the samples are signed
        #: integers, False if they are unsigned.
        self.signed: bool

        #: Number of samples per second (Hz).  Commonly 44,100 or
        #: 48,000.
        self.frequency: int
        
        raise PyOggError("AudioFile is an Abstract Base Class "+
                         "and should not be instantiated") 
    
    def as_array(self) -> Any:
        """Returns the buffer as a NumPy array.

        The shape of the returned array is in units of (number of
        samples per channel, number of channels).

        The data type is either 8-bit or 16-bit integers,
        depending on bytes_per_sample.

        The buffer is not copied, but rather the NumPy array
        shares the memory with the buffer.

        :rtype: numpy.array

        """
        # Assumes that self.buffer is a one-dimensional array of
        # bytes and that channels are interleaved.
        
        import numpy # type: ignore
        
        assert self.buffer is not None
        assert self.channels is not None

        # The following code assumes that the bytes in the buffer
        # represent 8-bit or 16-bit ints.  Ensure the number of
        # bytes per sample matches that assumption.
        assert self.bytes_per_sample == 1 or self.bytes_per_sample == 2

        # Create a dictionary mapping bytes per sample to numpy data
        # types.  The first key is the signedness, the second key is
        # the number of bytes per sample.
        dtype = {
            # signed
            True: {
                1: numpy.int8,
                2: numpy.int16
            },
            # unsigned
            False: {
                1: numpy.uint8,
                2: numpy.uint16
            }
        }
        
        # Convert the ctypes buffer to a NumPy array
        array = numpy.frombuffer(
            self.buffer,
            dtype=dtype[self.signed][self.bytes_per_sample]
        )

        # Reshape the array
        return array.reshape(
            (len(self.buffer)
             // self.bytes_per_sample
             // self.channels,
             self.channels)
        )
