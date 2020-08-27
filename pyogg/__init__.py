import builtins
import collections
import copy
import ctypes
import random
import struct
from . import ogg
from .ogg import PyOggError, PYOGG_OGG_AVAIL

from . import vorbis
from.vorbis import PYOGG_VORBIS_AVAIL, PYOGG_VORBIS_FILE_AVAIL, PYOGG_VORBIS_ENC_AVAIL

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

    class VorbisFileStream:
        def __init__(self, path):
            self.vf = vorbis.OggVorbis_File()
            error = vorbis.ov_fopen(path, ctypes.byref(self.vf))
            if error != 0:
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error))
                           
            info = vorbis.ov_info(ctypes.byref(self.vf), -1)

            #: Number of channels in audio file.
            self.channels = info.contents.channels

            #: Number of samples per second (per channel).  Always
            #  48,000.
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
            """get_buffer() -> bytesBuffer, bufferLength

            Returns None when all data has been read from the file.

            """
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

        
    class OpusFileStream:
        def __init__(self, path):
            """Opens an OggOpus file as a stream.

            path should be a string giving the filename of the file to
            open.  Unicode file names may not work correctly.

            An exception will be raised if the file cannot be opened
            correctly.

            """ 
            error = ctypes.c_int()

            self.of = opus.op_open_file(ogg.to_char_p(path), ctypes.pointer(error))

            if error.value != 0:
                self.of = None
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error.value))

            #: Number of channels in audio file
            self.channels = opus.op_channel_count(self.of, -1)

            #: Total PCM Length
            self.pcm_size = opus.op_pcm_total(self.of, -1)

            #: Number of samples per second (per channel)
            self.frequency = 48000

            # The buffer size should be (per channel) large enough to
            # hold 120ms (the largest possible Opus frame) at 48kHz.
            # See https://opus-codec.org/docs/opusfile_api-0.7/group__stream__decoding.html#ga963c917749335e29bb2b698c1cb20a10
            self.buffer_size = self.frequency // 1000 * 120 * self.channels
            self.Buf = opus.opus_int16 * self.buffer_size
            self._buf = self.Buf()
            self.buffer_ptr = ctypes.cast(
                ctypes.pointer(self._buf),
                opus.opus_int16_p
            )

            #: Bytes per sample
            self.bytes_per_sample = ctypes.sizeof(opus.opus_int16)

        def __del__(self):
            if self.of is not None:
                opus.op_free(self.of)

        def get_buffer(self):
            """Obtains the next frame of PCM samples.

            Returns an array of signed 16-bit integers.  If the file
            is in stereo, the left and right channels are interleaved.

            Returns None when all data has been read.

            The array that is returned should be either processed or
            copied before the next call to get_buffer() or
            get_buffer_as_array() as the array's memory is reused for
            each call.

            """
            # Read the next frame
            samples_read = opus.op_read(
                self.of,
                self.buffer_ptr,
                self.buffer_size,
                None
            )

            # Check for errors
            if samples_read < 0:
                raise PyOggError(
                    "Failed to read OpusFileStream.  Error {:d}".format(samples_read)
                )

            # Check if we've reached the end of the stream
            if samples_read == 0:
                return None

            # Cast the pointer to opus_int16 to an array of the
            # correct size
            result_ptr = ctypes.cast(
                self.buffer_ptr,
                ctypes.POINTER(opus.opus_int16 * (samples_read*self.channels))
            )

            # Convert the array to Python bytes
            return bytes(result_ptr.contents)

        def get_buffer_as_array(self):
            """Provides the buffer as a NumPy array.

            Note that the underlying data type is 16-bit signed
            integers.

            Does not copy the underlying data, so the returned array
            should either be processed or copied before the next call
            to get_buffer() or get_buffer_as_array().

            """
            import numpy

            # Read the next samples from the stream
            buf = self.get_buffer()

            # Check if we've come to the end of the stream
            if buf is None:
                return None

            # Convert the bytes buffer to a NumPy array
            array = numpy.frombuffer(
                buf,
                dtype=numpy.int16
            )

            # Reshape the array
            return array.reshape(
                (len(buf)
                 // self.bytes_per_sample
                 // self.channels,
                 self.channels)
            )

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

if PYOGG_OPUS_AVAIL:
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
            print(f"OpusEncoder.encode() called with {len(pcm_bytes)} bytes")
            
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

        
    class OpusBufferedEncoder(OpusEncoder):
        def __init__(self):
            super().__init__()
            
            self._frame_size_ms = None
            self._frame_size_bytes = None
            
            # To reduce copying, buffer is a double-ended queue of
            # bytes-objects
            self._buffer = collections.deque()

            # Total number of bytes in the buffer.
            self._buffer_size = 0

            
        def set_frame_size(self, frame_size):
            """ Set the desired frame duration (in milliseconds).

            Valid options are 2.5, 5, 10, 20, 40, or 60ms.

            """

            # Ensure the frame size is valid.  Compare frame size in
            # units of 0.1ms to avoid floating point comparison
            if int(frame_size*10) not in [25, 50, 100, 200, 400, 600]:
                raise PyOggError(
                    "Frame size ({:f}) not one of ".format(frame_size)+
                    "the acceptable values"
                )
            
            self._frame_size_ms = frame_size

            self._calc_frame_size()

            
        def set_sampling_frequency(self, samples_per_second):
            super().set_sampling_frequency(samples_per_second)
            self._calc_frame_size()

            
        def encode(self, pcm_bytes, flush=False):
            """Produces Opus-encoded packets from buffered PCM.

            First, pcm_bytes are appended to the end of the internal buffer.

            Then, while there are sufficient bytes in the buffer,
            frames will be encoded.

            This method returns a list, where each item in the list is
            an Opus-encoded frame stored as a bytes-object.

            If insufficient samples are passed in for the specified
            frame size, then an empty list will be returned.

            If flush is set to True, the buffer will be entirely
            emptied and, in the case that there remains PCM for only a
            partial final frame, the PCM will be completed with
            silence to make a complete final frame.

            """
            # Get the encoded packets
            results = self.encode_with_samples(pcm_bytes, flush=flush)

            # Strip the sample lengths
            stripped_results = [encoded_packet for
                                encoded_packet, _ in results]

            return stripped_results

        def encode_with_samples(self, pcm_bytes, flush=False, callback=None):
            """Gets encoded packets and their number of samples.

            This method returns a list, where each item in the list is
            a tuple.  The first item in the tuple is an Opus-encoded
            frame stored as a bytes-object.  The second item in the
            tuple is the number of samples encoded (excluding
            silence).

            If `callback` is supplied then this method will instead
            return an empty list but call the callback for every
            Opus-encoded frame that would have been returned as a
            list.  This option has the desireable property of
            eliminating the copying of the encoded packets, which is
            required in order to form a list.  The callback should
            take two arguments, the encoded frame (a Python bytes
            object) and the number of samples encoded per channel (an
            int).  The user must either process or copy the data as
            the data may be overwritten once the callback terminates.

            """
            self._buffer.append(pcm_bytes)
            self._buffer_size += len(pcm_bytes)

            results = []
            while True:
                # Get PCM from the buffer
                result = self._get_next_frame(add_silence=flush)

                # Check if we've sufficient bytes in the buffer
                if result is None:
                    break

                # Separate the components of the result
                pcm_to_encode, samples = result
                
                # Encode the PCM
                encoded_packet = super().encode(pcm_to_encode)

                if callback is None:
                    # Create a deep copy (otherwise the contents will be
                    # overwritten if there is a next call to encode
                    encoded_packet_copy = copy.deepcopy(encoded_packet)

                    # Append the copy of the encoded packet
                    results.append((encoded_packet_copy, samples))
                else:
                    # Call the callback with the encoded packet; it is
                    # the user's responsibility to copy the data if
                    # required.
                    callback(encoded_packet, samples)

            return results

                
        def _calc_frame_size(self):
            """Calculates the number of bytes in a frame.

            If the frame size (in milliseconds) and the number of
            samples per seconds have already been specified, then the
            frame size in bytes is set.  Otherwise, this method does
            nothing.

            The frame size is measured in bytes required to store the
            sample.

            """
            if (self._frame_size_ms is None
                or self._samples_per_second is None):
                return
            
            self._frame_size_bytes = (
                self._frame_size_ms
                * self._samples_per_second
                // 1000
                * ctypes.sizeof(opus.opus_int16)
                * self._channels
            )
                

        def _get_next_frame(self, add_silence=False):
            """Gets the next Opus-encoded frame.

            Returns a tuple where the first item is the Opus-encoded
            frame and the second item is the number of encoded samples
            (per channel).

            Returns None if insufficient data is available.

            """
            next_frame = bytes()
            samples = 0
            
            # Ensure frame size has been specified
            if self._frame_size_bytes is None:
                raise PyOggError(
                    "Desired frame size hasn't been set.  Perhaps "+
                    "encode() was called before set_frame_size() "+
                    "and set_sampling_frequency()?"
                )

            # Check if there's insufficient data in the buffer to fill
            # a frame.
            if self._frame_size_bytes > self._buffer_size:
                if len(self._buffer) == 0:
                    # No data at all in buffer
                    return None
                if add_silence:
                    # Get all remaining data
                    while len(self._buffer) != 0:
                        next_frame += self._buffer.popleft()
                    self._buffer_size = 0
                    # Store number of samples (per channel) of actual
                    # data
                    samples = (
                        len(next_frame)
                        // self._channels
                        // ctypes.sizeof(opus.opus_int16)
                    )
                    print("OpusBufferedEncoder._get_next_frame(): Samples (adding silence):", samples)
                    # Fill remainder of frame with silence
                    bytes_remaining = self._frame_size_bytes - len(next_frame)
                    next_frame += b'\x00' * bytes_remaining
                    return (next_frame, samples)
                else:
                    # Insufficient data to fill a frame and we're not
                    # adding silence
                    return None

            bytes_remaining = self._frame_size_bytes
            while bytes_remaining > 0:
                if len(self._buffer[0]) <= bytes_remaining:
                    # Take the whole first item
                    buffer_ = self._buffer.popleft()
                    next_frame += buffer_
                    bytes_remaining -= len(buffer_)
                    self._buffer_size -= len(buffer_)
                else:
                    # Take only part of the buffer

                    # TODO: This could be more efficiently
                    # implemented.  Rather than appending back the
                    # remaining data, we could just update an index
                    # saying where we were up to in regards to the
                    # first entry of the buffer.
                    buffer_ = self._buffer.popleft()
                    next_frame += buffer_[:bytes_remaining]
                    self._buffer_size -= bytes_remaining
                    # And put the unused part back into the buffer
                    self._buffer.appendleft(buffer_[bytes_remaining:])
                    bytes_remaining = 0

            # Calculate number of samples (per channel)
            samples = (
                len(next_frame)
                // self._channels
                // ctypes.sizeof(opus.opus_int16)
            )
            print("Samples (no silence):", samples)

            return (next_frame, samples)
                    
                    
        
    class OpusDecoder:
        def __init__(self):
            self._decoder = None
            self._channels = None
            self._samples_per_second = None
            self._pcm_buffer = None
            self._pcm_buffer_ptr = None
            self._pcm_buffer_size_int = None

        # TODO: Check if there is clean up that we need to do when
        # closing a decoder.
        
        #
        # User visible methods
        #

        def set_channels(self, n):

            """Set the number of channels.

            n must be either 1 or 2.

            The decoder is capable of filling in either mono or
            interleaved stereo pcm buffers.

            """
            if self._decoder is None:
                if n < 0 or n > 2:
                    raise PyOggError(
                        "Invalid number of channels in call to "+
                        "set_channels()"
                    )
                self._channels = n
                print(f"self._channels = {self._channels}")
            else:
                raise PyOggError(
                    "Cannot change the number of channels after "+
                    "the decoder was created.  Perhaps "+
                    "set_channels() was called after decode()?"
                )
            self._create_pcm_buffer()

        def set_sampling_frequency(self, samples_per_second):
            """Set the number of samples (per channel) per second.

            samples_per_second must be one of 8000, 12000, 16000,
            24000, or 48000.

            Internally Opus stores data at 48000 Hz, so that should be
            the default value for Fs. However, the decoder can
            efficiently decode to buffers at 8, 12, 16, and 24 kHz so
            if for some reason the caller cannot use data at the full
            sample rate, or knows the compressed data doesn't use the
            full frequency range, it can request decoding at a reduced
            rate.

            """
            if self._decoder is None:
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
                    "the decoder was created.  Perhaps "+
                    "set_sampling_frequency() was called after decode()?"
                )
            self._create_pcm_buffer()

        def decode(self, encoded_bytes):
            """Decodes an Opus-encoded packet into PCM.

            """
            # If we haven't already created a decoder, do so now
            if self._decoder is None:
                self._decoder = self._create_decoder()

            # Create pointer to encoded bytes
            encoded_bytes_ptr = ctypes.cast(
                encoded_bytes,
                ctypes.POINTER(ctypes.c_ubyte)
            )

            # Store length of encoded bytes into int32
            len_int32 = opus.opus_int32(
                len(encoded_bytes)
            )

            # Check that we have a PCM buffer
            if self._pcm_buffer is None:
                raise PyOggError("PCM buffer was not configured.")

            # Decode the encoded frame
            result = opus.opus_decode(
                self._decoder,
                encoded_bytes_ptr,
                len_int32,
                self._pcm_buffer_ptr,
                self._pcm_buffer_size_int,
                0 # TODO: What's Forward Error Correction about?
            )

            # Check for any errors
            if result < 0:
                raise PyOggError(
                    "An error occurred while decoding an Opus-encoded "+
                    "packet: "+
                    opus.opus_strerror(result).decode("utf")
                )

            # Extract just the valid data as bytes
            end_valid_data = (
                result
                * ctypes.sizeof(opus.opus_int16)
                * self._channels
            )
            return bytes(self._pcm_buffer)[:end_valid_data]


        def decode_missing_packet(self, frame_duration):
            """ Obtain PCM data despite missing a frame.

            frame_duration is in milliseconds.

            """
            
            # Consider frame duration in units of 0.1ms in order to
            # avoid floating-point comparisons.
            if int(frame_duration*10) not in [25, 50, 100, 200, 400, 600]:
                raise PyOggError(
                    "Frame duration ({:f}) is not one of the accepted values".format(frame_duration)
                )

            # Calculate frame size
            frame_size = int(
                frame_duration
                * self._samples_per_second
                // 1000
            )

            # Store frame size as int
            frame_size_int = ctypes.c_int(frame_size)
            
            # Decode missing packet
            result = opus.opus_decode(
                self._decoder,
                None,
                0,
                self._pcm_buffer_ptr,
                frame_size_int,
                0 # TODO: What is this Forward Error Correction about?
            )
                
            # Check for any errors
            if result < 0:
                raise PyOggError(
                    "An error occurred while decoding an Opus-encoded "+
                    "packet: "+
                    opus.opus_strerror(result).decode("utf")
                )

            # Extract just the valid data as bytes
            end_valid_data = (
                result
                * ctypes.sizeof(opus.opus_int16)
                * self._channels
            )
            return bytes(self._pcm_buffer)[:end_valid_data]
        
        #
        # Internal methods
        #

        def _create_pcm_buffer(self):
            if (self._samples_per_second is None
                or self._channels is None):
                # We cannot define the buffer yet
                return
            
            # Create buffer to hold 120ms of samples.  See "opus_decode()" at
            # https://opus-codec.org/docs/opus_api-1.3.1/group__opus__decoder.html
            max_duration = 120 # milliseconds
            max_samples = max_duration * self._samples_per_second // 1000
            PCMBuffer = opus.opus_int16 * (max_samples * self._channels)
            self._pcm_buffer = PCMBuffer()
            self._pcm_buffer_ptr = (
                ctypes.cast(ctypes.pointer(self._pcm_buffer),
                            ctypes.POINTER(opus.opus_int16))
            )

            # Store samples per channel in an int
            self._pcm_buffer_size_int = ctypes.c_int(max_samples)

        def _create_decoder(self):
            # To create a decoder, we must first allocate resources for it.
            # We want Python to be responsible for the memory deallocation,
            # and thus Python must be responsible for the initial memory
            # allocation.

            # Check that the sampling frequency has been defined
            if self._samples_per_second is None:
                raise PyOggError(
                    "The sampling frequency was not specified before "+
                    "attempting to create an Opus decoder.  Perhaps "+
                    "decode() was called before set_sampling_frequency()?"
                )
            
            # The sampling frequency must be passed in as a 32-bit int
            samples_per_second = opus.opus_int32(self._samples_per_second)

            # Check that the number of channels has been defined
            if self._channels is None:
                raise PyOggError(
                    "The number of channels were not specified before "+
                    "attempting to create an Opus decoder.  Perhaps "+
                    "decode() was called before set_channels()?"
                )
            
            # The number of channels must also be passed in as a 32-bit int
            channels = opus.opus_int32(self._channels)

            # Obtain the number of bytes of memory required for the decoder
            size = opus.opus_decoder_get_size(channels);

            # Allocate the required memory for the decoder
            memory = ctypes.create_string_buffer(size)

            # Cast the newly-allocated memory as a pointer to a decoder.  We
            # could also have used opus.od_p as the pointer type, but writing
            # it out in full may be clearer.
            decoder = ctypes.cast(memory, ctypes.POINTER(opus.OpusDecoder))

            # Initialise the decoder
            error = opus.opus_decoder_init(
                decoder,
                samples_per_second,
                channels
            );
            print(f"Initialised decoder with {channels} channels")

            # Check that there hasn't been an error when initialising the
            # decoder
            if error != opus.OPUS_OK:
                raise PyOggError(
                    "An error occurred while creating the decoder: "+
                    opus.opus_strerror(error).decode("utf")
                )

            # Return our newly-created decoder
            return decoder

else:
    class OpusEncoder:
        def __init__(*args, **kw):
            raise PyOggError("The Opus library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")

    class OpusDecoder:
        def __init__(*args, **kw):
            raise PyOggError("The Opus library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")

if (PYOGG_OGG_AVAIL and PYOGG_OPUS_AVAIL):        
    class OggOpusWriter(OpusBufferedEncoder):
        """Encodes PCM data into an OggOpus file."""

        def __init__(self, f, custom_pre_skip=None):
            """Construct an OggOpusWriter.

            f may be either a string giving the path to the file, or
            an already-opened file handle.

            If f is an already-opened file handle, then it is the
            user's responsibility to close the file when they are
            finished with it.

            The Opus encoder requires an amount of "warm up".  When
            `custom_pre_skip` is None, the required amount of silence
            is automatically calculated and inserted.  If a custom
            (non-silent) pre-skip is desired, then `custom_pre_skip`
            should be specified as the number of samples (per
            channel).  It is then the user's responsibility to pass
            the non-silent pre-skip samples to `encode()`.

            """
            super().__init__()

            # Store the custom pre skip
            self._custom_pre_skip = custom_pre_skip
            
            self._i_opened_the_file = None
            if isinstance(f, str):
                self._file = builtins.open(f, 'wb')
                self._i_opened_the_file = True
            else:
                # Assume it's already opened file
                self._file = f

            # Create a new stream state with a random serial number
            self._stream_state = self._create_stream_state()

            # Create a packet (reused for each pass)
            self._ogg_packet = ogg.ogg_packet()
            self._packet_valid = False

            # Create a page (reused for each pass)
            self._ogg_page = ogg.ogg_page()
            
            # Counter for the number of packets written into Ogg stream
            self._count_packets = 0

            # Counter for the number of samples encoded into Opus
            # packets
            self._count_samples = 0
            
            # Flag to indicate if the headers have been written
            self._headers_written = False

            # Flag to indicate that the stream has been finished (the
            # EOS bit was set in a final packet)
            self._finished = False

            # Reference to the current encoded packet (written only
            # when we know if it the last)
            self._current_encoded_packet = None

            # DEBUG
            import wave
            self.wave_out = wave.open("out.wav", "wb")
            self.wave_out.setnchannels(2)
            self.wave_out.setsampwidth(2)
            self.wave_out.setframerate(48000)

            self.decoder = OpusDecoder()
            self.decoder.set_sampling_frequency(48000)
            self.decoder.set_channels(2)
            
            
        def __del__(self):
            print("OggOpusWriter.__del__(): closing")
            if not self._finished:
                self.close()

        #
        # User visible methods
        #

        def encode(self, pcm_bytes):
            """Encode the PCM data as Opus packets wrapped in an Ogg stream.

            """
            # Check that the stream hasn't already been finished
            if self._finished:
                raise PyOggError(
                    "Stream has already ended.  Perhaps close() was "+
                    "called too early?")
            
            # If we haven't already created an encoder, do so now
            if self._encoder is None:
                self._encoder = self._create_encoder()

            # If we haven't already written out the headers, do so
            # now.  Then, write a frame of silence to warm up the
            # encoder.
            if not self._headers_written:
                pre_skip = self._write_headers(self._custom_pre_skip)
                if self._custom_pre_skip is None:
                    self._write_silence(pre_skip)

            # Call the internal method to encode the bytes
            self._encode_to_oggopus(pcm_bytes)

            
        def _encode_to_oggopus(self, pcm_bytes, flush=False):
            print(f"OggOpusWriter._encode_to_oggopus(): called with {len(pcm_bytes)} bytes in sample")
            
            def handle_encoded_packet(encoded_packet, samples):
                # If the previous packet is valid, write it into the stream
                if self._packet_valid:
                    print("Packet is valid; writing")
                    self._write_packet()
                
                # Keep a copy of the current encoded packet
                self._current_encoded_packet = copy.deepcopy(encoded_packet)
                
                # Obtain a pointer to the encoded packet
                encoded_packet_ptr = ctypes.cast(
                    self._current_encoded_packet,
                    ctypes.POINTER(ctypes.c_ubyte)
                )

                # Increase the count of the number of samples written
                self._count_samples += samples
                print(f"count samples = {self._count_samples}")

                
                # Place data into the packet
                self._ogg_packet.packet = encoded_packet_ptr
                self._ogg_packet.bytes = len(self._current_encoded_packet)
                self._ogg_packet.b_o_s = 0
                self._ogg_packet.e_o_s = 0
                self._ogg_packet.granulepos = self._count_samples
                self._ogg_packet.packetno = self._count_packets
                print("granulepos:", self._ogg_packet.granulepos)

                # # DEBUG
                # # Convert pointer to bytes
                # # Get array length
                # length = self._ogg_packet.bytes
                # import numpy.ctypeslib
                # np_array = numpy.ctypeslib.as_array(
                #     self._ogg_packet.packet,
                #     shape = (length,)
                # )

                # # Write out pcm to wave
                # encoded_packet = np_array.tobytes()
                # pcm = self.decoder.decode(encoded_packet)
                # self.wave_out.writeframes(pcm)


                
                # Increase the counter of the number of packets
                # in the stream
                self._count_packets += 1

                # Mark the packet as valid
                self._packet_valid = True

            # Encode the PCM data into an Opus packet
            print(f"OggOpusWriter._encode_to_oggopus(): flush = {flush}")
            super().encode_with_samples(
                pcm_bytes,
                flush=flush,
                callback=handle_encoded_packet
            )

        def close(self):
            print("OggOpusWriter.close()")
            # Check we haven't already closed this stream
            if self._finished:
                # We're attempting to close an already closed stream,
                # do nothing more.
                return
            
            # Flush the underlying buffered encoder
            self._encode_to_oggopus(b"", flush=True)
            
            # The current packet must be the end of the stream, update
            # the packet's details
            self._ogg_packet.e_o_s = 1

            # Write the packet to the stream
            print("OggopusWriter.close(): writing a last packet -- should we check it's valid?") 
            self._write_packet()

            # Flush the stream of any unwritten pages
            self._flush()

            # Mark the stream as finished
            self._finished = True

            # Close the file if we opened it
            if self._i_opened_the_file:
                print("Closing file")
                self._file.close()
                self._i_opened_the_file = False

            # Clean up the Ogg-related memory
            ogg.ogg_stream_clear(self._stream_state)
        
            # Clean up the reference to the encoded packet (as it must
            # now have been written)
            del self._current_encoded_packet
            
        #
        # Internal methods
        #

        def _create_random_serial_no(self):
            sizeof_c_int = ctypes.sizeof(ctypes.c_int)
            min_int = -2**(sizeof_c_int*8-1)
            max_int = 2**(sizeof_c_int*8-1)-1
            serial_no = ctypes.c_int(random.randint(min_int, max_int))

            return serial_no

        def _create_stream_state(self):
            # Create a random serial number
            serial_no = self._create_random_serial_no()

            # Create an ogg_stream_state
            ogg_stream_state = ogg.ogg_stream_state()

            # Initialise the stream state
            ogg.ogg_stream_init(
                ctypes.pointer(ogg_stream_state),
                serial_no
            )

            return ogg_stream_state

        def _make_identification_header(self, pre_skip, input_sampling_rate=0):
            """Make the OggOpus identification header.

            An input_sampling rate may be set to zero to mean 'unspecified'.

            Only channel mapping family 0 is currently supported.
            This allows mono and stereo signals.

            See https://tools.ietf.org/html/rfc7845#page-12 for more
            details.

            """
            signature = b"OpusHead"
            version = 1
            output_channels = self._channels
            output_gain = 0
            channel_mapping_family = 0
            data = struct.pack(
                "<BBHIHB",
                version,
                output_channels,
                pre_skip,
                input_sampling_rate,
                output_gain,
                channel_mapping_family
            )

            return signature+data
                   
        def _write_identification_header_packet(self, custom_pre_skip):
            if custom_pre_skip is not None:
                # Use the user-specified amount of pre-skip
                pre_skip = custom_pre_skip
            else:
                # Obtain the algorithmic delay of the Opus encoder.  See
                # page 27 of https://tools.ietf.org/html/rfc7845
                delay = opus.opus_int32()
                result = opus.opus_encoder_ctl(
                    self._encoder,
                    opus.OPUS_GET_LOOKAHEAD_REQUEST,
                    ctypes.pointer(delay)
                )
                if result != opus.OPUS_OK:
                    raise PyOggError(
                        "Failed to obtain the algorithmic delay of "+
                        "the Opus encoder: "+
                        opus.opus_strerror(result).decode("utf")
                    )
                delay_samples = delay.value

                # Extra samples are recommended.  See
                # https://tools.ietf.org/html/rfc7845#page-27
                extra_samples = 120

                # We will just fill a whole frame with silence.  Calculate
                # the minimum frame length, which we'll use as the
                # pre-skip.
                frame_durations = [2.5, 5, 10, 20, 40, 60] # milliseconds
                frame_lengths = [
                    x * self._samples_per_second // 1000
                    for x in frame_durations
                ]
                for frame_length in frame_lengths:
                    if frame_length > delay_samples + extra_samples:
                        pre_skip = frame_length
                        break

            # Create the identification header
            id_header = self._make_identification_header(
                pre_skip = pre_skip
            )

            # Specify the packet containing the identification header
            self._ogg_packet.packet = ctypes.cast(id_header, ogg.c_uchar_p)
            self._ogg_packet.bytes = len(id_header)
            self._ogg_packet.b_o_s = 1
            self._ogg_packet.e_o_s = 0
            self._ogg_packet.granulepos = 0
            self._ogg_packet.packetno = self._count_packets
            self._count_packets += 1

            # Write the identification header
            result = ogg.ogg_stream_packetin(
                self._stream_state,
                self._ogg_packet
            )

            if result != 0:
                raise PyOggError(
                    "Failed to write Opus identification header"
                )

            return pre_skip

        def _make_comment_header(self):
            """Make the OggOpus comment header.

            See https://tools.ietf.org/html/rfc7845#page-22 for more
            details.

            """
            signature = b"OpusTags"
            vendor_string = b"ENCODER=PyOgg"
            vendor_string_length = struct.pack("<I",len(vendor_string))
            user_comments_length = struct.pack("<I",0)

            return (
                signature
                + vendor_string_length
                + vendor_string
                + user_comments_length
            )

        def _write_comment_header_packet(self):
            # Specify the comment header
            comment_header = self._make_comment_header()

            # Specify the packet containing the identification header
            self._ogg_packet.packet = ctypes.cast(comment_header, ogg.c_uchar_p)
            self._ogg_packet.bytes = len(comment_header)
            self._ogg_packet.b_o_s = 0
            self._ogg_packet.e_o_s = 0
            self._ogg_packet.granulepos = 0
            self._ogg_packet.packetno = self._count_packets
            self._count_packets += 1

            # Write the header
            result = ogg.ogg_stream_packetin(
                self._stream_state,
                self._ogg_packet
            )

            if result != 0:
                raise PyOggError(
                    "Failed to write Opus comment header"
                )

        def _write_page(self):
            """ Write page to file """
            print("OggOpusWriter writing a page.")
            self._file.write(
                bytes(self._ogg_page.header[0:self._ogg_page.header_len])
            )
            self._file.write(
                bytes(self._ogg_page.body[0:self._ogg_page.body_len])
            )

        def _flush(self):
            """ Flush all pages to the file. """
            print("OggOpusWriter._flush() called")
            while ogg.ogg_stream_flush(
                    ctypes.pointer(self._stream_state),
                    ctypes.pointer(self._ogg_page)) != 0:
                print("Flushing a page")
                self._write_page()
            
        def _write_headers(self, custom_pre_skip):
            """ Write the two Opus header packets."""
            print("OggOpusWriter writing the two identificaiton headers")
            pre_skip = self._write_identification_header_packet(
                custom_pre_skip
            )
            self._write_comment_header_packet()

            # Store that the headers have been written
            self._headers_written = True

            # Write out pages to file to ensure that the headers are
            # the only packets to appear on the first page.  If this
            # is not done, the file cannot be read by the library
            # opusfile.
            self._flush()

            return pre_skip

        def _write_packet(self):
            print("OggOpusWriter._write_packet(): adding a packet to the stream")


            # DEBUG
            # Convert pointer to bytes
            # Get array length
            length = self._ogg_packet.bytes
            import numpy.ctypeslib
            np_array = numpy.ctypeslib.as_array(
                self._ogg_packet.packet,
                shape = (length,)
            )
            
            # Write out pcm to wave
            encoded_packet = np_array.tobytes()
            pcm = self.decoder.decode(encoded_packet)
            self.wave_out.writeframes(pcm)
                
            print("writing granulepos:", self._ogg_packet.granulepos)

            
            # Place the packet into the stream
            result = ogg.ogg_stream_packetin(
                self._stream_state,
                self._ogg_packet
            )

            # Check for errors
            if result != 0:
                raise PyOggError(
                    "Error while placing packet in Ogg stream"
                )

            # Write out pages to file
            while ogg.ogg_stream_pageout(
                    ctypes.pointer(self._stream_state),
                    ctypes.pointer(self._ogg_page)) != 0:
                print("OggOpusWriter._write_packet() calling _write_page()")
                self._write_page()

        def _write_silence(self, samples):
            """ Write a frame of silence. """
            silence_length = (
                samples
                * self._channels
                * ctypes.sizeof(opus.opus_int16)
            )
            silence_pcm = b"\x00" * silence_length
            self._encode_to_oggopus(silence_pcm)
            
else:
    class OggOpusWriter:
        def __init__(*args, **kw):
            if not PYOGG_OGG_AVAIL:
                raise PyOggError("The Ogg library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")
            raise PyOggError("The Opus library was't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")
        

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

            #: Number of channels in audio file.
            self.channels = None

            #: Number of samples per second (per channel).  For
            #  example, 44100.
            self.frequency = None

            self.total_samples = None

            #: Raw PCM data from audio file.
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

            #: Length of buffer
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

            #: Number of channels in audio file.
            self.channels = None

            #: Number of samples per second (per channel).  For
            #  example, 44100.
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
            """Returns the buffer and its length.

            Returns [buffer, buffer_length] or None if all data has
            been read from the file.

            """
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
    """Changes the maximum size for stream buffers.

    Initial value 8192.
    """
    global PYOGG_STREAM_BUFFER_SIZE
    PYOGG_STREAM_BUFFER_SIZE = size
