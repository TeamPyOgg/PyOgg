import pytest
import pyogg
import os

# Function to create an encoded packet
def get_encoded_packet(samples_per_second=48000,
                       application="audio",
                       channels=1,
                       duration_ms=20):
    encoder = pyogg.OpusEncoder()
    encoder.set_application(application)
    encoder.set_sampling_frequency(samples_per_second)
    encoder.set_channels(channels)

    # Create a sample of silence
    bytes_per_sample = 2
    buf = (
        b"\x00"
        * bytes_per_sample
        * channels
        * (samples_per_second // 1000)
        * duration_ms
    )

    # Encode the sample
    encoded_packet = encoder.encode(buf)

    return encoded_packet


# Function to create an decoder and decode a encode packet
def init_decoder(encoded_packet=None,
                 samples_per_second=48000,
                 channels=1,
                 set_sampling_frequency=True,
                 set_channels=True,
                 decode_packet=True) -> pyogg.OpusDecoder:
    decoder = pyogg.OpusDecoder()
    if set_sampling_frequency:
        decoder.set_sampling_frequency(samples_per_second)
    if set_channels:
        decoder.set_channels(channels)

    if decode_packet:
        # Decode the encoded packet
        decoder.decode(encoded_packet)
        
    return decoder


def test_decode() -> None:
    # Create encoded packet
    samples_per_second = 48000
    channels = 2
    duration_ms = 10
    encoded_packet = get_encoded_packet(
        samples_per_second = samples_per_second,
        channels = channels,
        duration_ms = duration_ms
    )

    # Create decoder and decode packet
    decoder = init_decoder(
        channels = channels,
        decode_packet = False
    )
    pcm = decoder.decode(encoded_packet)

    # Calculate expected length
    bytes_per_sample = 2
    expected_length = (
        duration_ms
        * samples_per_second // 1000
        * channels
        * bytes_per_sample
    )

    # Check length is as expected
    assert len(pcm) == expected_length

    
def test_decode_missing_packet() -> None:
    samples_per_second = 48000
    channels = 2
    duration_ms = 20
    encoded_packet = get_encoded_packet(
        samples_per_second = samples_per_second,
        channels = channels,
        duration_ms = duration_ms
    )
    
    decoder = init_decoder(
        encoded_packet,
        channels = channels,
    )
    
    pcm = decoder.decode_missing_packet(duration_ms)
    
    bytes_per_sample = 2
    expected_length = (
        duration_ms
        * samples_per_second // 1000
        * channels
        * bytes_per_sample
    )
        
    assert len(pcm) == expected_length

    # Check that there's an error on invalid packet size
    invalid_duration_ms = 99
    with pytest.raises(pyogg.PyOggError):
        decoder.decode_missing_packet(invalid_duration_ms)
    

def test_invalid_number_of_channels() -> None:
    with pytest.raises(pyogg.PyOggError):
        decoder = init_decoder(None, channels=3)

def test_change_number_of_channels() -> None:
    encoded_packet = get_encoded_packet()
    decoder = init_decoder(encoded_packet)
    with pytest.raises(pyogg.PyOggError):
        decoder.set_channels(1)

def test_invalid_sampling_frequency() -> None:
    with pytest.raises(pyogg.PyOggError):
        decoder = init_decoder(None, samples_per_second=44100)

def test_change_sampling_frequency() -> None:
    encoded_packet = get_encoded_packet()
    decoder = init_decoder(encoded_packet)
    with pytest.raises(pyogg.PyOggError):
        decoder.set_sampling_frequency(24000)

def test_sampling_frequency_not_set() -> None:
    with pytest.raises(pyogg.PyOggError):
        decoder = init_decoder(None, set_sampling_frequency=False)

def test_channels_not_set() -> None:
    with pytest.raises(pyogg.PyOggError):
        decoder = init_decoder(None, set_channels=False)

def test_pcm_buffer_not_configured() -> None:
    decoder = pyogg.OpusDecoder()
    decoder._decoder = "invalid"
    with pytest.raises(pyogg.PyOggError):
        decoder.decode(memoryview(bytearray(b"")))
