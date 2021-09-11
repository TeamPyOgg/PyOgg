import pytest
import pyogg

from config import Config


def test_error_in_filename() -> None:
    # Load a non-existant file
    filename = "does-not-exist.opus"
    with pytest.raises(pyogg.PyOggError):
        opus_file = pyogg.OpusFile(filename)
    
# FIXME: This shouldn't be a source of error, but it currently is.
# This works in macOS and probably Linux, but not Windows.
# def test_unicode_filename(pyogg_config: Config):
#     filename = str(
#         pyogg_config.rootdir
#         / "examples/unicode filename 🎵.opus"
#     )
#     opus_file = pyogg.OpusFile(filename)
        
def test_as_array(pyogg_config: Config) -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
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

    
def test_as_bytes(pyogg_config: Config) -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
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


def test_output_via_wav(pyogg_config: Config) -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.opus"
    )
    opus_file = pyogg.OpusFile(filename)

    import wave
    out_filename = str(
        pyogg_config.outdir
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


def test_from_memory(pyogg_config: Config) -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.opus"
    )
    # Load the file into memory, then into OpusFile.
    with open(filename, "rb") as f:
        from_memory = pyogg.OpusFile(f.read())
    # For comparison, load the file directly with OpusFile.
    from_file = pyogg.OpusFile(filename)
    assert bytes(from_memory.buffer) == bytes(from_file.buffer)
