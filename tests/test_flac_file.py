import pytest
import pyogg

def test_error_in_filename() -> None:
    # Load a non-existant file
    filename = "does-not-exist.flac"
    with pytest.raises(pyogg.PyOggError):
        flac_file = pyogg.FlacFile(filename)
    

def test_as_array(pyogg_config) -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(pyogg_config.rootdir / "examples/left-right-demo-5s.flac")
    flac_file = pyogg.FlacFile(filename)

    # Test that the loaded file is indeed 5 seconds long (using
    # as_array())
    expected_duration_seconds = 5
    samples_per_second = flac_file.frequency
    expected_duration_samples = (
        expected_duration_seconds
        * samples_per_second
    )
    duration_samples = flac_file.as_array().shape[0]
    assert duration_samples == expected_duration_samples

    
def test_as_bytes(pyogg_config) -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(pyogg_config.rootdir / "examples/left-right-demo-5s.flac")
    flac_file = pyogg.FlacFile(filename)

    # Test that the loaded file is indeed 5 seconds long (using
    # the buffer member variable)
    expected_duration_seconds = 5
    samples_per_second = flac_file.frequency
    channels = flac_file.channels
    bytes_per_sample = flac_file.bytes_per_sample
    expected_duration_bytes = (
        expected_duration_seconds
        * samples_per_second
        * bytes_per_sample
        * channels
    )
    duration_bytes = len(bytes(flac_file.buffer))
    assert duration_bytes == expected_duration_bytes


def test_output_via_wav(pyogg_config) -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(pyogg_config.rootdir / "examples/left-right-demo-5s.flac")
    flac_file = pyogg.FlacFile(filename)

    import wave
    out_filename = str(
        pyogg_config.outdir
        / "test_flac_file__test_output_via_wav.wav"
    )
    wave_out = wave.open(
        out_filename,
        "wb"
    )
    wave_out.setnchannels(flac_file.channels)
    wave_out.setsampwidth(flac_file.bytes_per_sample)
    wave_out.setframerate(flac_file.frequency)
    wave_out.writeframes(flac_file.buffer)
