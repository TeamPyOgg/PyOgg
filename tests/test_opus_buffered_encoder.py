import pytest
import pyogg
import os
from typing import Callable

os.chdir(os.path.dirname(__file__))

# Function to create an encoder and encode a sample of silence
def init_encoder(samples_per_second:int = 48000,
                 application: str = "audio",
                 channels: int = 1,
                 frame_size: int = 20, #ms
                 duration_ms: int = 60, #ms
                 set_sampling_frequency: bool = True,
                 set_application: bool = True,
                 set_channels: bool = True,
                 set_frame_size: bool = True,
                 callback: Callable[[bytes, int], None] = None
                 ) -> pyogg.OpusBufferedEncoder:
    encoder = pyogg.OpusBufferedEncoder()
    if set_application:
        encoder.set_application(application)
    if set_sampling_frequency:
        encoder.set_sampling_frequency(samples_per_second)
    if set_channels:
        encoder.set_channels(channels)
    if set_frame_size:
        encoder.set_frame_size(frame_size)

    # Create a sample of silence
    bytes_per_sample = 2
    buf = (
        b"\x00"
        * bytes_per_sample
        * channels
        * (samples_per_second // 1000)
        * duration_ms
    )

    if callback is None:
        # Encode the sample
        _ = encoder.encode_with_buffering(buf)
    else:
        # Encode with callback
        encoder.encode_with_samples(buf, callback=callback)
                                    
    return encoder
    

def test_encode() -> None:
    encoder = init_encoder()


def test_callback() -> None:
    # Calculate expected number of samples
    frame_size_ms = 10
    samples_per_second = 48000
    expected_samples = (
        frame_size_ms
        * samples_per_second // 1000
    )

    # Calculate the expected length of the decoded packet
    bytes_per_sample = 2
    channels = 2
    expected_pcm_length = (
        expected_samples
        * bytes_per_sample
        * channels
    )
    
    # Create a decoder to test that the encoded packets are valid
    decoder = pyogg.OpusDecoder()
    decoder.set_sampling_frequency(samples_per_second)
    decoder.set_channels(channels)
    
    # Specify the callback that will receive the encoded packets
    def callback(encoded_packet, samples):
        assert len(encoded_packet) > 0
        assert samples == expected_samples

        # Check encoded packet is valid
        pcm = decoder.decode(encoded_packet)
        assert len(pcm) == expected_pcm_length

    # Create the encoder
    encoder = init_encoder(
        channels = channels,
        frame_size = frame_size_ms,
        callback = callback
    )
    

def test_invalid_frame_size() -> None:
    with pytest.raises(pyogg.PyOggError):
        encoder = init_encoder(frame_size=15)
    

def test_frame_size_not_set() -> None:
    with pytest.raises(pyogg.PyOggError):
        encoder = init_encoder(set_frame_size=False)
