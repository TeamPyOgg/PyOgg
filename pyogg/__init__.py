import ctypes
from . import ogg
from .ogg import PyOggError, PYOGG_OGG_AVAIL

from . import vorbis
from.vorbis import PYOGG_VORBIS_AVAIL, PYOGG_VORBIS_FILE_AVAIL

from . import opus
from.opus import PYOGG_OPUS_AVAIL, PYOGG_OPUS_FILE_AVAIL, PYOGG_OPUS_ENC_AVAIL

from . import flac
from .flac import PYOGG_FLAC_AVAIL

from itertools import chain

def _to_char_p(string):
    try:
        return ctypes.c_char_p(string.encode("utf-8"))
    except:
        return ctypes.c_char_p(string)

def _resize_array(array, new_size):
    return (array._type_*new_size).from_address(ctypes.addressof(array))

PYOGG_STREAM_BUFFER_SIZE = 8192

if (PYOGG_OGG_AVAIL and PYOGG_VORBIS_AVAIL and PYOGG_VORBIS_FILE_AVAIL):
    class VorbisFile:
        def __init__(self, path):
            vf = vorbis.OggVorbis_File()
            error = vorbis.libvorbisfile.ov_fopen(vorbis.to_char_p(path), ctypes.byref(vf))
            if error != 0:
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error))
            
            info = vorbis.libvorbisfile.ov_info(ctypes.byref(vf), -1)

            self.channels = info.contents.channels

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

            self.buffer = b"".join(self.buffer_array)

            vorbis.libvorbisfile.ov_clear(ctypes.byref(vf))

            self.buffer_length = len(self.buffer)

    class VorbisFileStream:
        def __init__(self, path):
            self.vf = vorbis.OggVorbis_File()
            error = vorbis.ov_fopen(path, ctypes.byref(self.vf))
            if error != 0:
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error))
                           
            info = vorbis.ov_info(ctypes.byref(self.vf), -1)

            self.channels = info.contents.channels

            self.frequency = info.contents.rate

            array = (ctypes.c_char*(PYOGG_STREAM_BUFFER_SIZE*self.channels))()

            self.buffer_ = ctypes.cast(ctypes.pointer(array), ctypes.c_char_p)

            self.bitstream = ctypes.c_int()
            self.bitstream_pointer = ctypes.pointer(self.bitstream)

            self.exists = True

        def __del__(self):
            if self.exists:
                vorbis.ov_clear(ctypes.byref(self.vf))
            self.exists = False

        def clean_up(self):
            vorbis.ov_clear(ctypes.byref(self.vf))

            self.exists = False

        def get_buffer(self):
            """get_buffer() -> bytesBuffer, bufferLength"""
            if not self.exists:
                return None
            buffer = []
            total_bytes_written = 0
            
            while True:
                new_bytes = vorbis.ov_read(ctypes.byref(self.vf), self.buffer_, PYOGG_STREAM_BUFFER_SIZE*self.channels - total_bytes_written, 0, 2, 1, self.bitstream_pointer)
                
                array_ = ctypes.cast(self.buffer_, ctypes.POINTER(ctypes.c_char*(PYOGG_STREAM_BUFFER_SIZE*self.channels))).contents
                
                buffer.append(array_.raw[:new_bytes])

                total_bytes_written += new_bytes

                if new_bytes == 0 or total_bytes_written >= PYOGG_STREAM_BUFFER_SIZE*self.channels:
                    break

            out_buffer = b"".join(buffer)

            if total_bytes_written == 0:
                self.clean_up()
                return(None)

            return(out_buffer, total_bytes_written)
else:
    class VorbisFile:
        def __init__(*args, **kw):
            if not PYOGG_OGG_AVAIL:
                raise PyOggError("The Ogg library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")
            raise PyOggError("The Vorbis libraries weren't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")

    class VorbisFileStream:
        def __init__(*args, **kw):
            if not PYOGG_OGG_AVAIL:
                raise PyOggError("The Ogg library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")
            raise PyOggError("The Vorbis libraries weren't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")



if (PYOGG_OGG_AVAIL and PYOGG_OPUS_AVAIL and PYOGG_OPUS_FILE_AVAIL):
    class OpusFile:
        def __init__(self, path):
            error = ctypes.c_int()

            of = opus.op_open_file(ogg.to_char_p(path), ctypes.pointer(error))

            if error.value != 0:
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error.value))

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

        def as_array(self):
            """Returns the buffer as a NumPy array with the correct shape, where
            the shape is in units of (number of samples per channel,
            number of channels).
            """

            import numpy

            bytes_per_sample = ctypes.sizeof(opus.opus_int16)

            return numpy.ctypeslib.as_array(
                self.buffer,
                (self.buffer_length
                 // bytes_per_sample
                 // self.channels,
                 self.channels)
            )

    class OpusFileStream:
        def __init__(self, path):
            error = ctypes.c_int()

            self.of = opus.op_open_file(ogg.to_char_p(path), ctypes.pointer(error))

            if error.value != 0:
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error.value))

            self.channels = opus.op_channel_count(self.of, -1)

            self.pcm_size = opus.op_pcm_total(self.of, -1)

            self.frequency = 48000

            self.bfarr_t = opus.opus_int16*(PYOGG_STREAM_BUFFER_SIZE*self.channels*2)

            self.buffer = ctypes.cast(ctypes.pointer(self.bfarr_t()),opus.opus_int16_p)

            self.ptr = ctypes.cast(ctypes.pointer(self.buffer), ctypes.POINTER(ctypes.c_void_p))

            self.ptr_init = self.ptr.contents.value

        def get_buffer(self):
            if not hasattr(self, 'ptr'):
                return None

            samples_read = ctypes.c_int(0)
            while True:
                self.ptr.contents.value = self.ptr_init + samples_read.value*self.channels*2
                ns = opus.op_read(self.of, self.buffer , PYOGG_STREAM_BUFFER_SIZE*self.channels,ogg.c_int_p())
                if ns == 0:
                    break
                samples_read.value += ns
                if samples_read.value*self.channels*2 + ns >= PYOGG_STREAM_BUFFER_SIZE:
                    break

            if samples_read.value == 0:
                self.clean_up()
                return None

            self.ptr.contents.value = self.ptr_init

            buf = ctypes.pointer(self.bfarr_t())

            buf[0] = ctypes.cast(self.buffer, ctypes.POINTER(self.bfarr_t))[0]

            return(buf, samples_read.value*self.channels*2)

        def clean_up(self):
            self.ptr.contents.value = self.ptr_init

            del self.ptr

            opus.op_free(self.of)

            
    class OpusEncoder:
        """Encodes PCM data into Opus frames."""
        def __init__(self):
            self._encoder_ptr = None
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

            The number of channels must be between 1 and 255.  Only
            values between 1 and 8 are currently well-defined in the
            Opus specification.

            """
            if self._encoder is None:
                if n < 0 or n > 255:
                    raise PyOggError(
                        "Invalid number of channels in call to "+
                        "set_channels()"
                    )
                self._channels = n
            else:
                raise PyOggError(
                    "Cannot set the number of channels.  Perhaps "+
                    "encode() was called before set_channels()?"
                )

        def set_sampling_frequency(self, samples_per_second):
            """Set the number of samples (per channel) per second.

            This must be one of 8000, 12000, 16000, 24000, or 48000.
            """
            if self._encoder is None:
                self._samples_per_second = samples_per_second
            else:
                raise PyOggError(
                    "Cannot set sampling frequency.  "+
                    "Perhaps encode() was called before "+
                    "set_sampling_frequency()?"
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
                    "Cannot set application.  Perhaps encode() "+
                    "was called before set_applicaiton()?"
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
            if frame_duration not in [25, 50, 100, 200, 400, 600]:
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
                    opus.opus_strerror(error).decode("utf")
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

        
    class OpusDecoder:
        def __init__(self):
            pass


    class OggOpusWriter:

            """Encodes PCM data into an OggOpus file.""" 

else:
    class OpusFile:
        def __init__(*args, **kw):
            if not PYOGG_OGG_AVAIL:
                raise PyOggError("The Ogg library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")
            raise PyOggError("The Opus libraries weren't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")

    class OpusFileStream:
        def __init__(*args, **kw):
            if not PYOGG_OGG_AVAIL:
                raise PyOggError("The Ogg library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")
            raise PyOggError("The Opus libraries weren't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")

if PYOGG_FLAC_AVAIL:
    class FlacFile:
        def write_callback(self,decoder, frame, buffer, client_data):
            multi_channel_buf = _resize_array(buffer.contents, self.channels)
            arr_size = frame.contents.header.blocksize
            if frame.contents.header.channels >= 2:
                arrays = []
                for i in range(frame.contents.header.channels):
                    arr = ctypes.cast(multi_channel_buf[i], ctypes.POINTER(flac.FLAC__int32*arr_size)).contents
                    arrays.append(arr[:])

                arr = list(chain.from_iterable(zip(*arrays)))
                
                self.buffer[self.buffer_pos : self.buffer_pos + len(arr)] = arr[:]
                self.buffer_pos += len(arr)
                
            else:
                arr = ctypes.cast(multi_channel_buf[0], ctypes.POINTER(flac.FLAC__int32*arr_size)).contents
                self.buffer[self.buffer_pos : self.buffer_pos + arr_size] = arr[:]
                self.buffer_pos += arr_size
            return 0

        def metadata_callback(self,decoder, metadata, client_data):
            if not self.buffer:
                self.total_samples = metadata.contents.data.stream_info.total_samples
                self.channels = metadata.contents.data.stream_info.channels
                self.buffer = (flac.FLAC__int16*(self.total_samples * self.channels * 2))()
                self.frequency = metadata.contents.data.stream_info.sample_rate

        def error_callback(self,decoder, status, client_data):
            raise PyOggError("An error occured during the process of decoding. Status enum: {}".format(flac.FLAC__StreamDecoderErrorStatusEnum[status]))
        
        def __init__(self, path):
            self.decoder = flac.FLAC__stream_decoder_new()

            self.client_data = ctypes.c_void_p()

            self.channels = None

            self.frequency = None

            self.total_samples = None

            self.buffer = None

            self.buffer_pos = 0

            write_callback_ = flac.FLAC__StreamDecoderWriteCallback(self.write_callback)

            metadata_callback_ = flac.FLAC__StreamDecoderMetadataCallback(self.metadata_callback)

            error_callback_ = flac.FLAC__StreamDecoderErrorCallback(self.error_callback)

            init_status = flac.FLAC__stream_decoder_init_file(self.decoder,
                                          _to_char_p(path),
                                          write_callback_,
                                          metadata_callback_,
                                          error_callback_,
                                          self.client_data)

            if init_status: # error
                raise PyOggError("An error occured when trying to open '{}': {}".format(path, flac.FLAC__StreamDecoderInitStatusEnum[init_status]))

            metadata_status = (flac.FLAC__stream_decoder_process_until_end_of_metadata(self.decoder))
            if not metadata_status: # error
                raise PyOggError("An error occured when trying to decode the metadata of {}".format(path))
            
            stream_status = (flac.FLAC__stream_decoder_process_until_end_of_stream(self.decoder))
            if not stream_status: # error
                raise PyOggError("An error occured when trying to decode the audio stream of {}".format(path))

            flac.FLAC__stream_decoder_finish(self.decoder)

            self.buffer_length = len(self.buffer)

    class FlacFileStream:
        def write_callback(self,decoder, frame, buffer, client_data):
            multi_channel_buf = _resize_array(buffer.contents, self.channels)
            arr_size = frame.contents.header.blocksize
            if frame.contents.header.channels >= 2:
                arrays = []
                for i in range(frame.contents.header.channels):
                    arr = ctypes.cast(multi_channel_buf[i], ctypes.POINTER(flac.FLAC__int32*arr_size)).contents
                    arrays.append(arr[:])

                arr = list(chain.from_iterable(zip(*arrays)))
                
                self.buffer = (flac.FLAC__int16*len(arr))(*arr)
                self.bytes_written = len(arr) * 2
                
            else:
                arr = ctypes.cast(multi_channel_buf[0], ctypes.POINTER(flac.FLAC__int32*arr_size)).contents
                self.buffer = (flac.FLAC__int16*len(arr))(*arr[:])
                self.bytes_written = arr_size * 2
            return 0

        def metadata_callback(self,decoder, metadata, client_data):
            self.total_samples = metadata.contents.data.stream_info.total_samples
            self.channels = metadata.contents.data.stream_info.channels
            self.frequency = metadata.contents.data.stream_info.sample_rate

        def error_callback(self,decoder, status, client_data):
            raise PyOggError("An error occured during the process of decoding. Status enum: {}".format(flac.FLAC__StreamDecoderErrorStatusEnum[status]))
        
        def __init__(self, path):
            self.decoder = flac.FLAC__stream_decoder_new()

            self.client_data = ctypes.c_void_p()

            self.channels = None

            self.frequency = None

            self.total_samples = None

            self.buffer = None

            self.bytes_written = None

            self.write_callback_ = flac.FLAC__StreamDecoderWriteCallback(self.write_callback)

            self.metadata_callback_ = flac.FLAC__StreamDecoderMetadataCallback(self.metadata_callback)

            self.error_callback_ = flac.FLAC__StreamDecoderErrorCallback(self.error_callback)

            init_status = flac.FLAC__stream_decoder_init_file(self.decoder,
                                          _to_char_p(path),
                                          self.write_callback_,
                                          self.metadata_callback_,
                                          self.error_callback_,
                                          self.client_data)

            if init_status: # error
                raise PyOggError("An error occured when trying to open '{}': {}".format(path, flac.FLAC__StreamDecoderInitStatusEnum[init_status]))

            metadata_status = (flac.FLAC__stream_decoder_process_until_end_of_metadata(self.decoder))
            if not metadata_status: # error
                raise PyOggError("An error occured when trying to decode the metadata of {}".format(path))

        def get_buffer(self):
            if (flac.FLAC__stream_decoder_get_state(self.decoder) == 4): # end of stream
                return None
            stream_status = (flac.FLAC__stream_decoder_process_single(self.decoder))
            if not stream_status: # error
                raise PyOggError("An error occured when trying to decode the audio stream of {}".format(path))

            buffer_ = ctypes.pointer(self.buffer)

            return(buffer_, self.bytes_written)

        def clean_up(self):
            flac.FLAC__stream_decoder_finish(self.decoder)
else:
    class FlacFile:
        def __init__(*args, **kw):
            raise PyOggError("The FLAC libraries weren't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")

    class FlacFileStream:
        def __init__(*args, **kw):
            raise PyOggError("The FLAC libraries weren't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")

def pyoggSetStreamBufferSize(size):
    global PYOGG_STREAM_BUFFER_SIZE
    PYOGG_STREAM_BUFFER_SIZE = size
