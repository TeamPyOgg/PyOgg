import pytest
import pyogg
import os

def test_error_in_filename():
    # Load a non-existant file
    filename = "does-not-exist.opus"
    with pytest.raises(pyogg.PyOggError):
        opus_file = pyogg.OpusFile(filename)
    
# FIXME: This shouldn't be a source of error, but it currently is.
# This works in macOS and probably Linux, but not Windows.
# def test_unicode_filename():
#     filename = str(
#         pytest.pyogg.rootdir
#         / "examples/unicode filename 🎵.opus"
#     )
#     opus_file = pyogg.OpusFile(filename)
        
def test_as_array():
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pytest.pyogg.rootdir
        / "examples/left-right-demo-5s.opus"
    )

    opus_file = pyogg.OpusFile(filename)

    # Test that the loaded file is indeed 5 seconds long (using
    # as_array())
    expected_duration_seconds = 5
    samples_per_second = opus_file.frequency
    expected_duration_samples = (
        expected_duration_seconds
        * samples_per_second
    )
    duration_samples = opus_file.as_array().shape[0]
    assert duration_samples == expected_duration_samples

    
def test_as_bytes():
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pytest.pyogg.rootdir
        / "examples/left-right-demo-5s.opus"
    )
    opus_file = pyogg.OpusFile(filename)

    # Test that the loaded file is indeed 5 seconds long (using
    # the buffer member variable)
    expected_duration_seconds = 5
    samples_per_second = opus_file.frequency
    channels = opus_file.channels
    bytes_per_sample = opus_file.bytes_per_sample
    expected_duration_bytes = (
        expected_duration_seconds
        * samples_per_second
        * bytes_per_sample
        * channels
    )
    duration_bytes = len(bytes(opus_file.buffer))
    assert duration_bytes == expected_duration_bytes


def test_output_via_wav():
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pytest.pyogg.rootdir
        / "examples/left-right-demo-5s.opus"
    )
    opus_file = pyogg.OpusFile(filename)

    import wave
    out_filename = str(
        pytest.pyogg.outdir
        / "test_opus_file__test_output_via_wav.wav"
    )
    wave_out = wave.open(
        out_filename,
        "wb"
    )
    wave_out.setnchannels(opus_file.channels)
    wave_out.setsampwidth(opus_file.bytes_per_sample)
    wave_out.setframerate(opus_file.frequency)
    wave_out.writeframes(opus_file.buffer)
