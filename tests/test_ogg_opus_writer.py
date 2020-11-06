import pytest
import pyogg
import os

os.chdir(os.path.dirname(__file__))

def test_zero_length_audio() -> None:
    # Save the audio using OggOpusWriter
    filename = "test_ogg_opus_writer__test_zero_length_audio.opus"
    encoder = pyogg.OpusBufferedEncoder()
    encoder.set_application("audio")
    encoder.set_sampling_frequency(48000)
    channels = 1
    encoder.set_channels(channels)
    encoder.set_frame_size(20) # milliseconds
    writer = pyogg.OggOpusWriter(filename, encoder)
    
    buf = memoryview(bytearray(b""))
    
    writer.write(buf)

    # Close the file
    writer.close()

    # Test the length of the output is 0
    opus_file = pyogg.OpusFile(filename)
    assert len(opus_file.buffer) == 0
   
   
def test_one_frame_audio() -> None:
    # Save the audio using OggOpusWriter
    filename = "test_ogg_opus_writer__test_one_frame_audio.opus"
    encoder = pyogg.OpusBufferedEncoder()
    encoder.set_application("audio")
    samples_per_second = 48000
    encoder.set_sampling_frequency(samples_per_second)
    channels = 1
    encoder.set_channels(channels)
    frame_size_ms = 20
    encoder.set_frame_size(frame_size_ms) # milliseconds
    frame_size_samples = frame_size_ms * samples_per_second // 1000
    writer = pyogg.OggOpusWriter(filename, encoder)
    
    # Two bytes per sample
    bytes_per_sample = 2
    buf = bytearray(
        b"\x00" * (bytes_per_sample * frame_size_samples)
    )
    
    writer.write(memoryview(buf))

    # Close the file
    writer.close()

    # Test the length of the output
    opus_file = pyogg.OpusFile(filename)
    assert len(opus_file.buffer) == bytes_per_sample * frame_size_samples
    

def test_n_frames_audio() -> None:
    # Number of frames to write
    n = 2
    
    # Save the audio using OggOpusWriter
    filename = f"test_ogg_opus_writer__test_{n}_frames_audio.opus"
    encoder = pyogg.OpusBufferedEncoder()
    encoder.set_application("audio")
    samples_per_second = 48000
    encoder.set_sampling_frequency(samples_per_second)
    channels = 1
    encoder.set_channels(channels)
    frame_size_ms = 20
    encoder.set_frame_size(frame_size_ms) # milliseconds
    frame_size_samples = frame_size_ms * samples_per_second // 1000
    writer = pyogg.OggOpusWriter(filename, encoder)
    
    # Two bytes per sample, two frames
    bytes_per_sample = 2
    buf = b"\x00" * (bytes_per_sample * frame_size_samples * n)
    
    writer.write(memoryview(buf))

    # Close the file
    writer.close()

    # Test the length of the output
    opus_file = pyogg.OpusFile(filename)
    assert len(opus_file.buffer) == bytes_per_sample * frame_size_samples * n
    
    
def test_duplicate_audio() -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = "../examples/left-right-demo-5s.opus"
    opus_file = pyogg.OpusFile(filename)
    
    # Save the audio using OggOpusWriter
    out_filename = "test_ogg_opus_writer__test_duplicate_audio.opus"
    encoder = pyogg.OpusBufferedEncoder()
    encoder.set_application("audio")
    encoder.set_sampling_frequency(48000)
    encoder.set_channels(2)
    encoder.set_frame_size(20) # milliseconds
    writer = pyogg.OggOpusWriter(out_filename, encoder)
    writer.write(opus_file.buffer)

def test_already_loaded_file() -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = "../examples/left-right-demo-5s.opus"
    opus_file = pyogg.OpusFile(filename)

    # Save the audio using OggOpusWriter
    out_filename = "test_ogg_opus_writer__test_duplicate_audio.opus"
    f = open(out_filename, "wb")
    encoder = pyogg.OpusBufferedEncoder()
    encoder.set_application("audio")
    encoder.set_sampling_frequency(48000)
    encoder.set_channels(2)
    encoder.set_frame_size(20) # milliseconds
    writer = pyogg.OggOpusWriter(f, encoder)
    writer.write(opus_file.buffer)

    # Close the file
    f.close()


def test_custom_pre_skip() -> None:
    # Save the audio using OggOpusWriter
    filename = "test_ogg_opus_writer__test_zero_length_audio.opus"
    samples_of_pre_skip = 500
    encoder = pyogg.OpusBufferedEncoder()
    encoder.set_application("audio")
    encoder.set_sampling_frequency(48000)
    channels = 1
    encoder.set_channels(channels)
    encoder.set_frame_size(20) # milliseconds
    writer = pyogg.OggOpusWriter(
        filename,
        encoder,
        custom_pre_skip=samples_of_pre_skip
    )

    # Create a buffer of silence 
    bytes_per_sample = 2
    buf = (
        b"\x00"
        * bytes_per_sample
        * channels
        * samples_of_pre_skip
    )
    
    writer.write(memoryview(buf))

    # Close the file
    writer.close()

    # Test the length of the output is 0
    opus_file = pyogg.OpusFile(filename)
    assert len(opus_file.buffer) == 0


# Error handling tests
# ====================

# Subclassing from 'str' is purely to eliminate mypy type errors
class MockFile(str): 
    def write(self, data):
        pass

    
def test_error_after_close() -> None:
    mock_file = MockFile()
    encoder = pyogg.OpusBufferedEncoder()
    encoder.set_application("audio")
    encoder.set_sampling_frequency(48000)
    encoder.set_channels(2)
    encoder.set_frame_size(20) # milliseconds
    writer = pyogg.OggOpusWriter(mock_file, encoder)
    writer.close()
    with pytest.raises(pyogg.PyOggError):
        writer.write(memoryview(b""))

        
def test_close_twice() -> None:
    mock_file = MockFile()
    encoder = pyogg.OpusBufferedEncoder()
    encoder.set_application("audio")
    encoder.set_sampling_frequency(48000)
    encoder.set_channels(2)
    encoder.set_frame_size(20) # milliseconds
    writer = pyogg.OggOpusWriter(mock_file, encoder)
    writer.close()
    writer.close()
