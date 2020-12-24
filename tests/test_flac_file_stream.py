import pytest
import pyogg

from config import Config

def test_error_in_filename() -> None:
    # Load a non-existant file
    filename = "does-not-exist.flac"
    with pytest.raises(pyogg.PyOggError):
        flac_stream = pyogg.FlacFileStream(filename)

        
def test_total_length(pyogg_config: Config) -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.flac"
    )
    
    # Open the file using FlacFileStream, which does not read the entire
    # file immediately.
    flac_stream = pyogg.FlacFileStream(filename)

    # Loop through the FlacFileStream until we've read all the data
    samples_read = 0
    while True:
        # Read the next part of the stream
        buf = flac_stream.get_buffer_as_array()

        # Check if we've reached the end of the stream
        if buf is None:
            break

        # Increment the number of samples read
        samples_read += buf.shape[0]

    expected_duration_seconds = 5
    samples_per_second = flac_stream.frequency
    expected_duration_samples = (
        expected_duration_seconds
        * samples_per_second
    )
    duration_samples = samples_read
    assert duration_samples == expected_duration_samples


def test_same_data_as_flac_file(pyogg_config) -> None:
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.flac"
    )
    
    # Open the file using FlacFile to read the entire file into memory
    flac_file = pyogg.FlacFile(filename)
    
    # Open the file (again) using FlacFileStream, which does not read
    # the entire file immediately.
    flac_stream = pyogg.FlacFileStream(filename)

    # Loop through the FlacFileStream until we've read all the data
    buf_all = bytes()
    while True:
        # Read the next part of the stream
        buf = flac_stream.get_buffer()

        # Check if we've reached the end of the stream
        if buf is None:
            break

        # Add the bytes we've read to buf_all.  Note that this
        # technique isn't efficient and shouldn't be used in
        # production code.
        buf_all += buf
        
    assert buf_all == bytes(flac_file.buffer)
    
    
def test_same_data_as_flac_file_using_as_array(pyogg_config):
    import numpy # type: ignore
    
    # Load the demonstration file that is exactly 5 seconds long
    filename = str(
        pyogg_config.rootdir
        / "examples/left-right-demo-5s.flac"
    )
    
    # Open the file using FlacFile to read the entire file into memory
    flac_file = pyogg.FlacFile(filename)
    
    # Open the file (again) using FlacFileStream, which does not read
    # the entire file immediately.
    flac_stream = pyogg.FlacFileStream(filename)

    # Loop through the FlacFileStream until we've read all the data
    buf_all = None
    while True:
        # Read the next part of the stream
        buf = flac_stream.get_buffer_as_array()

        # Check if we've reached the end of the stream
        if buf is None:
            break

        # Add the bytes we've read to buf_all.  Note that this
        # technique isn't efficient and shouldn't be used in
        # production code.
        if buf_all is None:
            buf_all = buf
        else:
            buf_all = numpy.concatenate(
                (buf_all, buf)
            )

    # Check that every byte is identical for both buffers
    assert numpy.all(buf_all == flac_file.as_array())
    
