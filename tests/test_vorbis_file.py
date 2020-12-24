import pytest
import pyogg
import os

from config import Config

def test_error_in_filename():
    # Load a non-existant file
    filename = "does-not-exist.ogg"
    with pytest.raises(pyogg.PyOggError):
        vorbis_file = pyogg.VorbisFile(filename)
    

def test_as_array(pyogg_config: "Config"):
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.ogg"
    )
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

    
def test_as_bytes(pyogg_config: "Config"):
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.ogg"
    )
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


def test_as_bytes_one_byte_per_sample(pyogg_config: "Config"):
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.ogg"
    )
    vorbis_file = pyogg.VorbisFile(filename, bytes_per_sample=1)

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


def test_bytes_per_sample(pyogg_config: "Config"):
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.ogg"
    )
    vorbis_file_1 = pyogg.VorbisFile(filename, bytes_per_sample=1)
    vorbis_file_2 = pyogg.VorbisFile(filename, bytes_per_sample=2)

    # Test that the buffer lengths differ by a factor of two.
    assert len(vorbis_file_2.buffer) == len(vorbis_file_1.buffer)*2
    

def test_output_via_wav(pyogg_config: "Config"):
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.ogg"
    )
    vorbis_file = pyogg.VorbisFile(filename)

    import wave
    out_filename = str(
        pyogg_config.outdir
        / "test_vorbis_file__test_output_via_wav.wav"
    )
    wave_out = wave.open(
        out_filename, 
        "wb"
    )
    wave_out.setnchannels(vorbis_file.channels)
    wave_out.setsampwidth(vorbis_file.bytes_per_sample)
    wave_out.setframerate(vorbis_file.frequency)
    wave_out.writeframes(vorbis_file.buffer)


def test_output_via_wav_one_byte_per_sample(pyogg_config: "Config"):
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.ogg"
    )
    vorbis_file = pyogg.VorbisFile(
        filename,
        bytes_per_sample = 1,
        signed = False
    )

    import wave
    out_filename = str(
        pyogg_config.outdir
        / "test_vorbis_file__test_output_via_wav_one_byte_per_sample.wav"
    )
    wave_out = wave.open(
        out_filename,
        "wb"
    )
    wave_out.setnchannels(vorbis_file.channels)
    wave_out.setsampwidth(vorbis_file.bytes_per_sample)
    wave_out.setframerate(vorbis_file.frequency)
    wave_out.writeframes(vorbis_file.buffer)
