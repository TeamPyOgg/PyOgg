import ctypes
import os
from typing import Callable

import pytest
import pyogg

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
                 callback: Callable[[memoryview, int, bool], None] = None,
                 flush: bool = False
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
    buf = bytearray(
        b"\x00"
        * bytes_per_sample
        * channels
        * (samples_per_second // 1000)
        * duration_ms
    )

    encoder.buffered_encode(
        memoryview(buf),
        flush=flush,
        callback=callback
    )
                                    
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
    index = 0
    def callback(encoded_packet: memoryview,
                 samples: int,
                 end_of_stream: bool) -> None:
        assert len(encoded_packet) > 0
        assert samples == expected_samples

        # Check encoded packet is valid
        pcm = decoder.decode(encoded_packet)
        assert len(pcm) == expected_pcm_length

        # Ignore the end of stream; it's tested below

    # Create the encoder
    encoder = init_encoder(
        channels = channels,
        frame_size = frame_size_ms,
        duration_ms = 60,
        callback = callback
    )
    

def test_eos_with_no_data() -> None:
    def callback(encoded_packet: memoryview,
                 samples: int,
                 end_of_stream: bool) -> None:
        assert samples == 0
        assert end_of_stream is True
        
    encoder = init_encoder(
        duration_ms = 0,
        callback = callback
    )

def test_eos_with_under_one_frame() -> None:
    def callback(encoded_packet: memoryview,
                 samples: int,
                 end_of_stream: bool) -> None:
        assert end_of_stream is True
        
    encoder = init_encoder(
        frame_size = 20,
        duration_ms = 19,
        callback = callback
    )
    
def test_eos_with_one_frame() -> None:
    def callback(encoded_packet: memoryview,
                 samples: int,
                 end_of_stream: bool) -> None:
        assert end_of_stream is True
        
    encoder = init_encoder(
        frame_size = 10,
        duration_ms = 10,
        callback = callback
    )
    
def test_eos_with_over_one_frame() -> None:
    samples_per_ms = 48000 // 1000
    frame_1_ms = 5
    frame_2_ms = 1
    
    index = 0
    expected_eos = [False, True]
    expected_samples = [samples_per_ms*frame_1_ms,
                        samples_per_ms*frame_2_ms]
    def callback(encoded_packet: memoryview,
                 samples: int,
                 end_of_stream: bool) -> None:
        nonlocal index
        assert end_of_stream is expected_eos[index]
        assert samples == expected_samples[index]
        index += 1
        
    encoder = init_encoder(
        frame_size = 5,
        duration_ms = frame_1_ms + frame_2_ms,
        callback = callback
    )
    
    
def test_invalid_frame_size() -> None:
    with pytest.raises(pyogg.PyOggError):
        encoder = init_encoder(frame_size=15)
    

def test_frame_size_not_set() -> None:
    with pytest.raises(pyogg.PyOggError):
        encoder = init_encoder(set_frame_size=False)
