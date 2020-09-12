import pytest
import pyogg

def test_error_in_filename():
    # Load a non-existant file
    filename = "does-not-exist.ogg"
    with pytest.raises(pyogg.PyOggError):
        vorbis_file = pyogg.VorbisFile(filename)
    

def test_as_array():
    # Load the demonstration file that is exactly 5 seconds long
    filename = "../examples/left-right-demo-5s.ogg"
    vorbis_file = pyogg.VorbisFile(filename)

    # Test that the loaded file is indeed 5 seconds long (using
    # as_array())
    expected_duration_seconds = 5
    samples_per_second = vorbis_file.frequency
    expected_duration_samples = (
        expected_duration_seconds
        * samples_per_second
    )
    duration_samples = vorbis_file.as_array().shape[0]
    assert duration_samples == expected_duration_samples

    
def test_as_bytes():
    # Load the demonstration file that is exactly 5 seconds long
    filename = "../examples/left-right-demo-5s.ogg"
    vorbis_file = pyogg.VorbisFile(filename)

    # Test that the loaded file is indeed 5 seconds long (using
    # the buffer member variable)
    expected_duration_seconds = 5
    samples_per_second = vorbis_file.frequency
    channels = vorbis_file.channels
    bytes_per_sample = vorbis_file.bytes_per_sample
    expected_duration_bytes = (
        expected_duration_seconds
        * samples_per_second
        * bytes_per_sample
        * channels
    )
    duration_bytes = len(vorbis_file.buffer)
    assert duration_bytes == expected_duration_bytes


def test_output_via_wav():
    # Load the demonstration file that is exactly 5 seconds long
    filename = "../examples/left-right-demo-5s.ogg"
    vorbis_file = pyogg.VorbisFile(filename)

    import wave
    wave_out = wave.open(
        "test_vorbis_file__test_output_via_wav.wav",
        "wb"
    )
    wave_out.setnchannels(vorbis_file.channels)
    wave_out.setsampwidth(vorbis_file.bytes_per_sample)
    wave_out.setframerate(vorbis_file.frequency)
    wave_out.writeframes(vorbis_file.buffer)
