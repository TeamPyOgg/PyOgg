from .pyogg_error import PyOggError

class AudioFile:
    def __init__(self):
        raise PyOggError("AudioFile is an Abstract Base Class "+
                         "and should not be instantiated") 
    
    def as_array(self):
        """Returns the buffer as a NumPy array.

        The shape of the returned array is in units of (number of
        samples per channel, number of channels).

        The data type is 16-bit signed integers.

        The buffer is not copied, but rather the NumPy array
        shares the memory with the buffer.

        """
        import numpy # type: ignore
        
        assert self.buffer is not None

        # Convert the bytes buffer to a NumPy array
        array = numpy.frombuffer(
            self.buffer,
            dtype=numpy.int16
        )

        # Reshape the array
        print("len(self.buffer):", len(self.buffer))
        return array.reshape(
            (len(self.buffer)
             // self.channels,
             self.channels)
        )
