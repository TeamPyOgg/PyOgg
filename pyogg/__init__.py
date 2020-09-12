import builtins
import collections
import copy
import ctypes
import random
import struct

from .pyogg_error import PyOggError

from . import ogg
from .ogg import PYOGG_OGG_AVAIL

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


#: PyOgg version number.  Versions should comply with PEP440.
__version__ = '0.6.14a7'

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

            #: Bytes per sample
            self.bytes_per_sample = 2 # TODO: Where is this actually defined?

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
    # OpusFile
    from .opus_file import OpusFile
    # OpusFileStream
    from .opus_file_stream import OpusFileStream

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
    # OpusEncoder
    from .opus_encoder import OpusEncoder
    # OpusBufferedEncoder
    from .opus_buffered_encoder import OpusBufferedEncoder
    # OpusDecoder
    from .opus_decoder import OpusDecoder

else:
    class OpusEncoder:
        def __init__(*args, **kw):
            raise PyOggError("The Opus library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")

    class OpusBufferedEncoder:
        def __init__(*args, **kw):
            raise PyOggError("The Opus library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")
        
    class OpusDecoder:
        def __init__(*args, **kw):
            raise PyOggError("The Opus library wasn't found or couldn't be loaded (maybe you're trying to use 64bit libraries with 32bit Python?)")

if (PYOGG_OGG_AVAIL and PYOGG_OPUS_AVAIL):        
    # OggOpusWriter
    from .ogg_opus_writer import OggOpusWriter
    
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
