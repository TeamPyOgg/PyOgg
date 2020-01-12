import ctypes
import numpy
import sys

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
    INTERLEAVED_BYTES_8BIT = 1
    INTERLEAVED_BYTES_16BIT = 2
##    INTERLEAVED_BYTES_32BIT = 4
##    INTERLEAVED_BYTES_64BIT = 5

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

        elif target_type == self.INTERLEAVED_BYTES_8BIT:
            if self.type == self.INTERLEAVED_BYTES_16BIT:
                as_numpy_array = (numpy.frombuffer(self.data, dtype=numpy.int16) // 256).astype(numpy.int8)
                return bytes(as_numpy_array)

            elif self.type == self.FLOAT_ARRAYS:
                as_interleaved_array = numpy.empty((self.samples * self.channels,), dtype=numpy.float32)
                for i in range(self.channels):
                    as_interleaved_array[i::self.channels] = self.data[i]

                out = numpy.ceil((as_interleaved_array + 1.0) * 127.5).astype(numpy.int8) - numpy.int8(128)
                return bytes(out)

        elif target_type == self.INTERLEAVED_BYTES_16BIT:
            if self.type == self.INTERLEAVED_BYTES_8BIT:
                as_numpy_array = (numpy.frombuffer(self.data, dtype=numpy.int8) * 256).astype(numpy.int16)
                return bytes(as_numpy_array)

            elif self.type == self.FLOAT_ARRAYS:
                as_interleaved_array = numpy.empty((self.samples * self.channels,), dtype=numpy.float32)
                for i in range(self.channels):
                    as_interleaved_array[i::self.channels] = self.data[i]

                out = numpy.ceil((as_interleaved_array + 1.0) * 32767.5).astype(numpy.int16) - numpy.int16(32768)
                return bytes(out)

        elif target_type == self.FLOAT_ARRAYS:
            if self.type == self.INTERLEAVED_BYTES_8BIT:
                as_numpy_array = ((numpy.frombuffer(self.data, dtype=numpy.int8) + numpy.uint8(128)).astype(numpy.float32) / 127.5) - 1.0
                out_type = (ctypes.c_float * self.samples) * self.channels
                out_arr_list = [(ctypes.c_float * self.samples)(*as_numpy_array[i::self.channels]) for i in range(self.channels)]
                out_arr = out_type(*out_arr_list)
                return out_arr

            elif self.type == self.INTERLEAVED_BYTES_16BIT:
                as_numpy_array = ((numpy.frombuffer(self.data, dtype=numpy.int16) + numpy.uint16(32768)).astype(numpy.float32) / 32767.5) - 1.0
                out_type = (ctypes.c_float * self.samples) * self.channels
                out_arr_list = [(ctypes.c_float * self.samples)(*as_numpy_array[i::self.channels]) for i in range(self.channels)]
                out_arr = out_type(*out_arr_list)
                return out_arr

    def as_bytes(self):
        if self.type == bytes:
            return self.data

class AudioFile:
    def read(self, num_of_bytes):
        raise NotImplementedError("read() is not supported")

    def write(self, data_bytes):
        raise NotImplementedError("write() is not supported")

    def get_channels(self):
        raise NotImplementedError("get_channels() is not supported")

    def get_frequency(self):
        raise NotImplementedError("get_frequency() is not supported")

    def get_samples(self):
        raise NotImplementedError("get_samples in not supported")

    def get_duration(self):
        raise NotImplementedError("get_duration() is not supported")

    def get_metadata(self):
        raise NotImplementedError("get_metadata() is not supported")

    def tell(self):
        raise NotImplementedError("tell() is not supported")

    def tell_time(self):
        raise NotImplementedError("tell_time() is not supported")

    def seek(self):
        raise NotImplementedError("seek() is not supported")

    def seek_time(self):
        raise NotImplementedError("seek_time() is not supported")

    def close(self):
        raise NotImplementedError("close() is not supported")

PYOGG_STREAM_BUFFER_SIZE = 8192

if (PYOGG_OGG_AVAIL and PYOGG_VORBIS_AVAIL and PYOGG_VORBIS_FILE_AVAIL):
    class VorbisFile(AudioFile):
        def __init__(self, path):
            self.vf = vorbis.OggVorbis_File()
            self.vf_ptr = ctypes.pointer(self.vf)
##            self.path_ptr = vorbis.to_char_p(path)

            self.path = path

            self._file = open(self.path, "rb")

            self._read_func_ptr = vorbis.read_func(self._read_callback)
            self._seek_func_ptr = vorbis.seek_func(self._seek_callback)
            self._close_func_ptr = vorbis.close_func(self._close_callback)
            self._tell_func_ptr = vorbis.tell_func(self._tell_callback)

            self._callbacks = vorbis.ov_callbacks(
                self._read_func_ptr,
                self._seek_func_ptr,
                self._close_func_ptr,
                self._tell_func_ptr
            )
            
            error = vorbis.libvorbisfile.ov_open_callbacks(self.vf_ptr, self.vf_ptr, None, 0, self._callbacks)
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

            #vorbis.libvorbisfile.ov_pcm_seek(self.vf_ptr, 0) # set position to 0 to prevent invalid tell values

            for i in range(comment.contents.comments):
                single_metadata = comment.contents.user_comments[i].decode()
                if "=" in single_metadata:
                    split_metadata = single_metadata.split("=")
                    self.metadata[split_metadata[0].upper()] = split_metadata[1]
                else:
                    if not "UNKNOWN_COMMENTS" in self.metadata:
                        self.metadata["UNKNOWN_COMMENTS"] = []
                    self.metadata["UNKNOWN_COMMENTS"].append(single_metadata)

        def _read_callback(self, buffer, byte_size, byte_count, data_source):
            read = self._file.read(byte_size * byte_count)
            ctypes.memmove(buffer, read, len(read))
            return len(read)

        def _seek_callback(self, data_source, offset, whence):
            self._file.seek(offset, whence)
            return 0

        def _close_callback(self, data_source):
            self._file.close()
            return 0

        def _tell_callback(self, data_source):
            return self._file.tell()

##        def read16(self, num_of_samples = None):
##            if not self.vf:
##                raise PyOggError("The file is closed")
##            
##            full_read = False
##            
##            if num_of_samples is None:
##                offset = vorbis.libvorbisfile.ov_pcm_tell(self.vf_ptr)
##                num_of_samples = self.samples - offset
##
##                full_read = True
##
##            if not num_of_samples:
##                return None
##
##            num_of_bytes = num_of_samples * 2 * self.channels
##
##            array = (ctypes.c_char * num_of_bytes)()
##
##            buffer_ = ctypes.cast(array, ctypes.POINTER(ctypes.c_char))
##
##            bitstream = ctypes.c_int()
##            bitstream_pointer = ctypes.pointer(bitstream)
##
##            if not full_read:                
##                new_bytes = vorbis.libvorbisfile.ov_read(self.vf_ptr, buffer_, num_of_bytes, 0, 2, 1, bitstream_pointer) # requesting floating point 32 bit data
##
##                new_samples = new_bytes // (2 * self.channels)
##
##                if new_bytes:
##                    return AudioData(bytes(array[:new_bytes]), AudioData.INTERLEAVED_BYTES_16BIT, new_samples, self.channels)
##                return None
##            
##            else:
##                out_datatype = (ctypes.c_float * num_of_samples) * self.channels
##                out_arr = out_datatype()
##                out_arr_pointers = [ctypes.cast(out_arr[i], ctypes.c_void_p) for i in range(self.channels)]
##                num_of_samples_copy = num_of_samples
##
##                total_samples = 0
##                
##                while num_of_samples_copy:
##                    new_samples = vorbis.libvorbisfile.ov_read_float(self.vf_ptr, buffer_, min(num_of_samples_copy, 1024), bitstream_pointer) # requesting floating point 32 bit data
##                    told = (vorbis.libvorbisfile.ov_pcm_tell(self.vf_ptr))
##                    total_samples += new_samples
##                    diff = told - total_samples
##
####                    if (diff):
####                        vorbis.ov_pcm_seek(self.vf_ptr, total_samples)
##
##                    print(told, total_samples, told == total_samples)
##                    if new_samples <= 0:
##                        break
##
##                    bytes_read = new_samples * ctypes.sizeof(ctypes.c_float)
##
##                    print(any(pcm[0][:bytes_read]))
##
##                    for i in range(self.channels):
##                        ctypes.memmove(out_arr_pointers[i], pcm[i], bytes_read)
##                        out_arr_pointers[i].value += bytes_read
##
##                    print(num_of_samples_copy, new_samples)
##
##                    num_of_samples_copy -= new_samples
##
##                print(f"total: {total_samples}")
##
##                return AudioData(out_arr, AudioData.FLOAT_ARRAYS, num_of_samples, self.channels)

        def tell(self):
            return vorbis.ov_pcm_tell(self.vf_ptr)

        def tell_time(self):
            return vorbis.ov_time_tell(self.vf_ptr)

        def seek(self, pos):
            return vorbis.ov_pcm_seek(self.vf_ptr, pos)

        def seek_time(self, time):
            return vorbis.ov_time_seek(self.vf_ptr, time)

        def seek_page(self, pos):
            return vorbis.ov_pcm_seek_page(self.vf_ptr, pos)

        def seek_time_page(self, time):
            return vorbis.ov_time_seek_page(self.vf_ptr, time)

        def seek_lap(self, pos):
            return vorbis.ov_pcm_seek_lap(self.vf_ptr, pos)

        def seek_time_lap(self, time):
            return vorbis.ov_time_seek_lap(self.vf_ptr, time)

        def seek_page_lap(self, pos):
            return vorbis.ov_pcm_seek_page_lap(self.vf_ptr, pos)

        def seek_time_page_lap(self, time):
            return vorbis.ov_time_seek_page_lap(self.vf_ptr, time)

        def read(self, num_of_samples = None, full_read = None):
            if not self.vf:
                raise PyOggError("The file is closed")
            
            if num_of_samples is None:
                offset = vorbis.libvorbisfile.ov_pcm_tell(self.vf_ptr)
                num_of_samples = self.samples - offset

                if full_read is None: full_read = True

            if not num_of_samples:
                return None

            pcm = ctypes.POINTER(ctypes.POINTER(ctypes.c_float))()

            buffer_ = ctypes.pointer(pcm)

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

                total_samples = 0
                
                while num_of_samples_copy:
                    new_samples = vorbis.libvorbisfile.ov_read_float(self.vf_ptr, buffer_, min(num_of_samples_copy, 1024), bitstream_pointer) # requesting floating point 32 bit data
##                    told = (vorbis.libvorbisfile.ov_pcm_tell(self.vf_ptr))
                    total_samples += new_samples
##                    diff = told - total_samples

##                    if (diff):
##                        vorbis.ov_pcm_seek(self.vf_ptr, total_samples)

                    if new_samples <= 0:
                        break

                    bytes_read = new_samples * ctypes.sizeof(ctypes.c_float)

                    for i in range(self.channels):
                        ctypes.memmove(out_arr_pointers[i], pcm[i], bytes_read)
                        out_arr_pointers[i].value += bytes_read

                    num_of_samples_copy -= new_samples

                if total_samples == 0:
                    return None

                return AudioData(out_arr, AudioData.FLOAT_ARRAYS, num_of_samples, self.channels)

        def __getattr__(self, name):
            if name == "buffer":
                read = self.read()
                self._deprecated_buffer = read.get_data(AudioData.INTERLEAVED_BYTES_16BIT) if read else None
                print("DeprecationWarning: Accessing the buffer won't be supported in a future update", file=sys.stderr)
                return self._deprecated_buffer

            elif name == "buffer_length":
                print("DeprecationWarning: Accessing buffer_length won't be supported in a future update", file=sys.stderr)
                return len(self._deprecated_buffer) if self._deprecated_buffer else 0

            raise AttributeError("VorbisFile doesn't have the attribute '{}'".format(name))

        def get_channels(self):
            return self.channels

        def get_frequency(self):
            return self.frequency

        def get_samples(self):
            return self.samples

        def get_duration(self):
            return self.duration

        def get_metadata(self):
            return self.metadata

        def close(self):
            if not self.vf:
                return
            vorbis.libvorbisfile.ov_clear(self.vf_ptr)
            self.vf = None

    class VorbisFileStream(VorbisFile):
        def __init__(self, path):
            print("DeprecationWarning: VorbisFileStream won't be supported in a future update", file=sys.stderr)
            super().__init__(path)
            self.exists = True

        def __del__(self):
            if self.exists:
                self.close()
            self.exists = False

        def clean_up(self):
            self.close()

            self.exists = False

        def get_buffer(self):
            """get_buffer() -> bytesBuffer, bufferLength"""
            if not self.exists:
                return None

            read = self.read(PYOGG_STREAM_BUFFER_SIZE*self.channels, True)

            out = read.get_data(AudioData.INTERLEAVED_BYTES_16BIT) if read else None
            
            if not out:
                self.clean_up()
                return None

            return (out, len(out))
        
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
