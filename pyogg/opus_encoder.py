import ctypes

from . import opus
from .pyogg_error import PyOggError

class OpusEncoder:
    """Encodes PCM data into Opus frames."""
    def __init__(self):
        self._encoder = None
        self._channels = None
        self._samples_per_second = None
        self._application = None
        self._encoder = None
        self._pcm_buffer = None
        self._max_bytes_per_frame = None
        self._output_buffer = None
        self._output_buffer_ptr = None

        # An output buffer of 4,000 bytes is recommended in
        # https://opus-codec.org/docs/opus_api-1.3.1/group__opus__encoder.html
        self.set_max_bytes_per_frame(4000)

    #
    # User visible methods
    #

    def set_channels(self, n):
        """Set the number of channels.

        n must be either 1 or 2.

        """
        if self._encoder is None:
            if n < 0 or n > 2:
                raise PyOggError(
                    "Invalid number of channels in call to "+
                    "set_channels()"
                )
            self._channels = n
        else:
            raise PyOggError(
                "Cannot change the number of channels after "+
                "the encoder was created.  Perhaps "+
                "set_channels() was called after encode()?"
            )

    def set_sampling_frequency(self, samples_per_second):
        """Set the number of samples (per channel) per second.

        This must be one of 8000, 12000, 16000, 24000, or 48000.

        Regardless of the sampling rate and number of channels
        selected, the Opus encoder can switch to a lower audio
        bandwidth or number of channels if the bitrate selected is
        too low. This also means that it is safe to always use 48
        kHz stereo input and let the encoder optimize the
        encoding.

        """
        if self._encoder is None:
            if samples_per_second in [8000, 12000, 16000, 24000, 48000]:
                self._samples_per_second = samples_per_second
            else:
                raise PyOggError(
                    "Specified sampling frequency "+
                    "({:d}) ".format(samples_per_second)+
                    "was not one of the accepted values"
                )
        else:
            raise PyOggError(
                "Cannot change the sampling frequency after "+
                "the encoder was created.  Perhaps "+
                "set_sampling_frequency() was called after encode()?"
            )

    def set_application(self, application):
        """Set the encoding mode.

        This must be one of 'voip', 'audio', or 'restricted_lowdelay'.

        'voip': Gives best quality at a given bitrate for voice
        signals. It enhances the input signal by high-pass
        filtering and emphasizing formants and
        harmonics. Optionally it includes in-band forward error
        correction to protect against packet loss. Use this mode
        for typical VoIP applications. Because of the enhancement,
        even at high bitrates the output may sound different from
        the input.

        'audio': Gives best quality at a given bitrate for most
        non-voice signals like music. Use this mode for music and
        mixed (music/voice) content, broadcast, and applications
        requiring less than 15 ms of coding delay.

        'restricted_lowdelay': configures low-delay mode that
        disables the speech-optimized mode in exchange for
        slightly reduced delay. This mode can only be set on an
        newly initialized encoder because it changes the codec
        delay.
        """
        if self._encoder is not None:
            raise PyOggError(
                "Cannot change the application after "+
                "the encoder was created.  Perhaps "+
                "set_application() was called after encode()?"
            )
        if application == "voip":
            self._application = opus.OPUS_APPLICATION_VOIP
        elif application == "audio":
            self._application = opus.OPUS_APPLICATION_AUDIO
        elif application == "restricted_lowdelay":
            self._application = opus.OPUS_APPLICATION_RESTRICTED_LOWDELAY
        else:
            raise PyOggError(
                "The application specification '{:s}' ".format(application)+
                "wasn't one of the accepted values."
            )

    def set_max_bytes_per_frame(self, max_bytes):
        """Set the maximum number of bytes in an encoded frame.

        Size of the output payload. This may be used to impose an
        upper limit on the instant bitrate, but should not be used
        as the only bitrate control.

        TODO: Use OPUS_SET_BITRATE to control the bitrate.

        """
        self._max_bytes_per_frame = opus.opus_int32(max_bytes)
        OutputBuffer = ctypes.c_ubyte * max_bytes
        self._output_buffer = OutputBuffer()
        self._output_buffer_ptr = (
            ctypes.cast(ctypes.pointer(self._output_buffer),
                        ctypes.POINTER(ctypes.c_ubyte))
        )

    def encode(self, pcm_bytes):
        """Encodes PCM data into an Opus frame.

        pcm_bytes must be formatted as bytes, with each sample
        taking two bytes (signed 16-bit integers; interleaved
        left, then right channels if in stereo).

        """
        # If we haven't already created an encoder, do so now
        if self._encoder is None:
            self._encoder = self._create_encoder()

        # Calculate the effective frame duration of the given PCM
        # data.  Calculate it in units of 0.1ms in order to avoid
        # floating point comparisons.
        bytes_per_sample = 2
        frame_size = (
            len(pcm_bytes) # bytes
            // bytes_per_sample
            // self._channels
        )
        frame_duration = (
            (10*frame_size)
            // (self._samples_per_second//1000)
        )

        # Check that we have a valid frame size
        if int(frame_duration) not in [25, 50, 100, 200, 400, 600]:
            raise PyOggError(
                "The effective frame duration ({:.1f} ms) "
                .format(frame_duration/10)+
                "was not one of the acceptable values."
            )

        # Create a pointer to the PCM data
        pcm_ptr = ctypes.cast(pcm_bytes,
                              ctypes.POINTER(opus.opus_int16))


        # Create an int giving the frame size per channel
        frame_size_int = ctypes.c_int(frame_size)

        # Encode PCM
        result = opus.opus_encode(
            self._encoder,
            pcm_ptr,
            frame_size_int,
            self._output_buffer_ptr,
            self._max_bytes_per_frame
        )

        # Check for any errors
        if result < 0:
            raise PyOggError(
                "An error occurred while encoding to Opus format: "+
                opus.opus_strerror(result).decode("utf")
            )

        # Extract just the valid data as bytes
        return bytes(self._output_buffer[:result])


    #
    # Internal methods
    #

    def _create_encoder(self):
        # To create an encoder, we must first allocate resources for it.
        # We want Python to be responsible for the memory deallocation,
        # and thus Python must be responsible for the initial memory
        # allocation.

        # Check that the application has been defined
        if self._application is None:
            raise PyOggError(
                "The application was not specified before "+
                "attempting to create an Opus encoder.  Perhaps "+
                "encode() was called before set_application()?"
            )
        application = self._application

        # Check that the sampling frequency has been defined
        if self._samples_per_second is None:
            raise PyOggError(
                "The sampling frequency was not specified before "+
                "attempting to create an Opus encoder.  Perhaps "+
                "encode() was called before set_sampling_frequency()?"
            )

        # The frequency must be passed in as a 32-bit int
        samples_per_second = opus.opus_int32(self._samples_per_second)

        # Check that the number of channels has been defined
        if self._channels is None:
            raise PyOggError(
                "The number of channels were not specified before "+
                "attempting to create an Opus encoder.  Perhaps "+
                "encode() was called before set_channels()?"
            )
        channels = self._channels

        # Obtain the number of bytes of memory required for the encoder
        size = opus.opus_encoder_get_size(channels);

        # Allocate the required memory for the encoder
        memory = ctypes.create_string_buffer(size)

        # Cast the newly-allocated memory as a pointer to an encoder.  We
        # could also have used opus.oe_p as the pointer type, but writing
        # it out in full may be clearer.
        encoder = ctypes.cast(memory, ctypes.POINTER(opus.OpusEncoder))

        # Initialise the encoder
        error = opus.opus_encoder_init(
            encoder,
            samples_per_second,
            channels,
            application
        )

        # Check that there hasn't been an error when initialising the
        # encoder
        if error != opus.OPUS_OK:
            raise PyOggError(
                "An error occurred while creating the encoder: "+
                opus.opus_strerror(error).decode("utf")
            )

        # Return our newly-created encoder
        return encoder
