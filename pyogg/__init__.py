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
            error, vf = vorbis.ov_fopen(path)
            if error != 0:
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error))
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

    class VorbisFileStream:
        def __init__(self, path):
            error, self.vf = vorbis.ov_fopen(path)
            if error != 0:
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error))
                           
            info = vorbis.ov_info(self.vf, -1)

            self.channels = info.contents.channels

            self.frequency = info.contents.rate

            array = (ctypes.c_char*(PYOGG_STREAM_BUFFER_SIZE*self.channels))()

            self.buffer_ = ctypes.cast(ctypes.pointer(array), ctypes.c_char_p)

            self.bitstream = ctypes.c_int()
            self.bitstream_pointer = ctypes.pointer(self.bitstream)

            del array

            self.exists = True

        def clean_up(self):
            del self.buffer_

            del self.bitstream

            del self.bitstream_pointer

            vorbis.ov_clear(self.vf)

            self.exists = False

        def get_buffer(self):
            """get_buffer() -> bytesBuffer, bufferLength"""
            if not self.exists:
                return None
            buffer = b""
            
            while True:
                new_bytes = vorbis.ov_read(self.vf, self.buffer_, PYOGG_STREAM_BUFFER_SIZE*self.channels - len(buffer), 0, 2, 1, self.bitstream_pointer)
                
                array_ = ctypes.cast(self.buffer_, ctypes.POINTER(ctypes.c_char*(PYOGG_STREAM_BUFFER_SIZE*self.channels))).contents
                
                if buffer:
                    buffer += array_.raw[:new_bytes]
                else:
                    buffer = array_.raw[:new_bytes]

                del array_

                if new_bytes == 0 or len(buffer) == PYOGG_STREAM_BUFFER_SIZE*self.channels:
                    break

            if len(buffer) == 0:
                self.clean_up()
                return(None)

            return(buffer, len(buffer))
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
