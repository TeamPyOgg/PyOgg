import ctypes
import warnings
import numpy

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

class AudioData:
    INTERLACED_BYTES_8BIT = 1
    INTERLACED_BYTES_16BIT = 2
##    INTERLACED_BYTES_32BIT = 4
##    INTERLACED_BYTES_64BIT = 5

    FLOAT_ARRAYS = 3
##    BYTE_ARRAY = 2
##    CHAR_ARRAY = 3
##    SHORT_ARRAY = 4
##    FLOAT_ARRAY_CHANNEL_ARRAY = 5
    
    def __init__(self, data, type, samples, channels):
        self.data = data
        self.type = type
        self.samples = samples
        self.channels = channels

    def get_data(self, target_type = None):
        if target_type == None or target_type == self.type:
            return self.data

        elif target_type == self.INTERLACED_BYTES_8BIT:
            if self.type == self.INTERLACED_BYTES_16BIT:
                as_numpy_array = (numpy.frombuffer(self.data, dtype=numpy.int16) // 256).astype(numpy.int8)
                return bytes(as_numpy_array)

            elif self.type == self.FLOAT_ARRAYS:
                as_interlaced_array = numpy.empty((self.samples * self.channels,), dtype=numpy.float32)
                for i in range(self.channels):
                    as_interlaced_array[i::self.channels] = self.data[i]

                out = numpy.ceil((as_interlaced_array + 1.0) * 127.5).astype(numpy.int8) - numpy.int8(128)
                print(out.shape)
                return bytes(out)

        elif target_type == self.INTERLACED_BYTES_16BIT:
            if self.type == self.INTERLACED_BYTES_8BIT:
                as_numpy_array = (numpy.frombuffer(self.data, dtype=numpy.int8) * 256).astype(numpy.int16)
                return bytes(as_numpy_array)

            elif self.type == self.FLOAT_ARRAYS:
                as_interlaced_array = numpy.empty((self.samples * self.channels,), dtype=numpy.float32)
                for i in range(self.channels):
                    as_interlaced_array[i::self.channels] = self.data[i]

                out = numpy.ceil((as_interlaced_array + 1.0) * 32767.5).astype(numpy.int16) - numpy.int16(32768)
                return bytes(out)

        elif target_type == self.FLOAT_ARRAYS:
            if self.type == self.INTERLACED_BYTES_8BIT:
                as_numpy_array = ((numpy.frombuffer(self.data, dtype=numpy.int8) + numpy.int8(128)).astype(numpy.float32) / 127.5) - 1.0
                out_type = (ctypes.c_float * self.samples) * self.channels
                print(as_numpy_array.shape, self.channels, self.samples)
                out_arr_list = [(ctypes.c_float * self.samples)(*as_numpy_array[i::self.channels]) for i in range(self.channels)]
                print(out_arr_list)
                out_arr = out_type(*out_arr_list)
                return out_arr

            elif self.type == self.INTERLACED_BYTES_16BIT:
                as_numpy_array = ((numpy.frombuffer(self.data, dtype=numpy.int16) + numpy.int16(32768)).astype(numpy.float32) / 32767.5) - 1.0
                out_type = (ctypes.c_float * self.samples) * self.channels
                print(as_numpy_array.shape)
                out_arr_list = [(ctypes.c_float * self.samples)(*as_numpy_array[i::self.channels]) for i in range(self.channels)]
                print(out_arr_list)
                out_arr = out_type(*out_arr_list)
                return out_arr

    def as_bytes(self):
        if self.type == bytes:
            return self.data

class AudioFile:
    def read(num_of_bytes):
        raise NotImplementedError("read() is not supported")

    def write(data_bytes):
        raise NotImplementedError("write() is not supported")

    def get_channels():
        raise NotImplementedError("get_channels() is not supported")

    def get_frequency():
        raise NotImplementedError("get_frequency() is not supported")

    def get_samples():
        raise NotImplementedError("get_samples in not supported")

    def get_duration():
        raise NotImplementedError("get_duration() is not supported")

    def get_metadata():
        raise NotImplementedError("get_metadata() is not supported")

    def close():
        raise NotImplementedError("close() is not supported")

PYOGG_STREAM_BUFFER_SIZE = 8192

if (PYOGG_OGG_AVAIL and PYOGG_VORBIS_AVAIL and PYOGG_VORBIS_FILE_AVAIL):
    class VorbisFile(AudioFile):
        def __init__(self, path):
            self.vf = vorbis.OggVorbis_File()
            self.vf_ptr = ctypes.byref(self.vf)
            self.path_ptr = vorbis.to_char_p(path)
            
            error = vorbis.libvorbisfile.ov_fopen(self.path_ptr, self.vf_ptr)
            if error != 0:
                if error == vorbis.OV_EREAD:
                    raise vorbis.OggVorbisError("A read from media returned an error.")
                if error == vorbis.OV_ENOTVORBIS:
                    raise vorbis.OggVorbisError("Bitstream does not contain any Vorbis data.")
                if error == vorbis.OV_EVERSION:
                    raise vorbis.OggVorbisError("Vorbis version mismatch.")
                if error == vorbis.OV_EBADHEADER:
                    raise vorbis.OggVorbisError("Invalid Vorbis bitstream header.")
                if error == vorbis.OV_EFAULT:
                    raise vorbis.OggVorbisError("Internal logic fault; indicates a bug or heap/stack corruption.")
                if error in vorbis.error_docs:
                    raise vorbis.OggVorbisError(vorbis.error_docs[error])
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error))
            
            info = vorbis.libvorbisfile.ov_info(self.vf_ptr, -1)

            if not info:
                raise vorbis.OggVorbisError("The file has been initialized improperly.")

            self.channels = info.contents.channels

            self.frequency = info.contents.rate

            self.samples = vorbis.libvorbisfile.ov_pcm_total(self.vf_ptr, -1)

            self.duration = vorbis.libvorbisfile.ov_time_total(self.vf_ptr, -1)

            self.metadata = {}

            comment = vorbis.libvorbisfile.ov_comment(self.vf_ptr, -1)

            vorbis.libvorbisfile.ov_pcm_seek(self.vf_ptr, 0) # set position to 0 to prevent invalid tell values

            for i in range(comment.contents.comments):
                single_metadata = comment.contents.user_comments[i].decode()
                if "=" in single_metadata:
                    split_metadata = single_metadata.split("=")
                    self.metadata[split_metadata[0].upper()] = split_metadata[1]
                else:
                    if not "UNKNOWN_COMMENTS" in self.metadata:
                        self.metadata["UNKNOWN_COMMENTS"] = []
                    self.metadata["UNKNOWN_COMMENTS"].append(single_metadata)
                

        def read(self, num_of_samples = None):
            full_read = False
            
            if num_of_samples is None:
                offset = vorbis.libvorbisfile.ov_pcm_tell(self.vf_ptr)
                num_of_samples = self.samples - offset

                full_read = True

            if not num_of_samples:
                return None

            pcm = ctypes.POINTER(ctypes.POINTER(ctypes.c_float))()

            buffer_ = ctypes.byref(pcm)

            bitstream = ctypes.c_int()
            bitstream_pointer = ctypes.pointer(bitstream)

            if not full_read:                
                new_samples = vorbis.libvorbisfile.ov_read_float(self.vf_ptr, buffer_, num_of_samples, bitstream_pointer) # requesting floating point 32 bit data

                if new_samples:
                    out_datatype = (ctypes.c_float * new_samples) * self.channels
                    out_arr = out_datatype()
                    for i in range(self.channels):
                        ctypes.memmove(out_arr[i], pcm[i], ctypes.sizeof(ctypes.c_float) * new_samples)
                    return AudioData(out_arr, AudioData.FLOAT_ARRAYS, new_samples, self.channels)
                return None
            
            else:
                out_datatype = (ctypes.c_float * num_of_samples) * self.channels
                out_arr = out_datatype()
                out_arr_pointers = [ctypes.cast(out_arr[i], ctypes.c_void_p) for i in range(self.channels)]
                num_of_samples_copy = num_of_samples
                
                while num_of_samples_copy:
                    new_samples = vorbis.libvorbisfile.ov_read_float(self.vf_ptr, buffer_, num_of_samples_copy, bitstream_pointer) # requesting floating point 32 bit data
                    if new_samples <= 0:
                        break

                    bytes_read = new_samples * ctypes.sizeof(ctypes.c_float)

                    for i in range(self.channels):
                        ctypes.memmove(out_arr_pointers[i], pcm[i], bytes_read)
                        out_arr_pointers[i].value += bytes_read

                    num_of_samples_copy -= bytes_read

                return AudioData(out_arr, AudioData.FLOAT_ARRAYS, num_of_samples, self.channels)

        def __getattr__(self, name):
            if name == "buffer":
                warnings.warn(DeprecationWarning("Accessing the buffer won't be supported in a future update"))
                return self.read().get_data(AudioData.INTERLACED_BYTES_16BIT)

            raise AttributeError("VorbisFile doesn't have the attribute '{}'".format(name))

        def get_channels(self):
            return self.channels

        def get_frequency(self):
            return self.frequency

        def get_samples():
            return self.samples

        def get_duration():
            return self.duration

        def get_metadata(self):
            return self.metadata

        def close(self):
            vorbis.libvorbisfile.ov_clear(ctypes.byref(self.vf))

    class VorbisFileStream:
        def __init__(self, path):
            self.vf = vorbis.OggVorbis_File()
            error = vorbis.ov_fopen(path, ctypes.byref(self.vf))
            if error != 0:
                raise PyOggError("file couldn't be opened or doesn't exist. Error code : {}".format(error))
                           
            info = vorbis.ov_info(ctypes.byref(self.vf), -1)

            self.channels = info.contents.channels

            self.frequency = info.contents.rate

            self.array = (ctypes.c_char*(PYOGG_STREAM_BUFFER_SIZE*self.channels))()

            self.buffer_ = ctypes.cast(ctypes.pointer(self.array), ctypes.c_char_p)

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

            new_bytes = 1
            
            while new_bytes and total_bytes_written < PYOGG_STREAM_BUFFER_SIZE*self.channels:
                new_bytes = vorbis.ov_read(ctypes.byref(self.vf), self.buffer_, PYOGG_STREAM_BUFFER_SIZE*self.channels - total_bytes_written, 0, 2, 1, self.bitstream_pointer)
                
                buffer.append(self.array.raw[:new_bytes])

                total_bytes_written += new_bytes

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



if (PYOGG_OPUS_AVAIL and PYOGG_OPUS_FILE_AVAIL):
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

            self.buffer_array = bfarr_t()

            self.buffer_ptr = ctypes.cast(ctypes.pointer(self.buffer_array),opus.opus_int16_p)

            self.buffer = self.buffer_ptr

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
