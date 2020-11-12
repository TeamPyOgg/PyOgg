import pytest
import pyogg
import os

os.chdir(os.path.dirname(__file__))

def test_error_in_filename():
    # Load a non-existant file
    filename = "does-not-exist.ogg"
    with pytest.raises(pyogg.PyOggError):
        vorbis_stream = pyogg.VorbisFileStream(filename)

        
def test_total_length():
    # Load the demonstration file that is exactly 5 seconds long
    filename = "../examples/left-right-demo-5s.ogg"
    
    # Open the file using VorbisFileStream, which does not read the entire
    # file immediately.
    vorbis_stream = pyogg.VorbisFileStream(filename)

    # Loop through the VorbisFileStream until we've read all the data
    samples_read = 0
    while True:
        # Read the next part of the stream
        buf = vorbis_stream.get_buffer_as_array()

        # Check if we've reached the end of the stream
        if buf is None:
            break

        # Increment the number of samples read
        samples_read += buf.shape[0]

    expected_duration_seconds = 5
    samples_per_second = vorbis_stream.frequency
    expected_duration_samples = (
        expected_duration_seconds
        * samples_per_second
    )
    duration_samples = samples_read
    assert duration_samples == expected_duration_samples


def test_same_data_as_vorbis_file():
    # Load the demonstration file that is exactly 5 seconds long
    filename = "../examples/left-right-demo-5s.ogg"

    # Open the file using VorbisFile to read the entire file into memory
    vorbis_file = pyogg.VorbisFile(filename)
    
    # Open the file (again) using VorbisFileStream, which does not read
    # the entire file immediately.
    vorbis_stream = pyogg.VorbisFileStream(filename)

    # Loop through the VorbisFileStream until we've read all the data
    buf_all = bytes()
    while True:
        # Read the next part of the stream
        buf = vorbis_stream.get_buffer()

        # Check if we've reached the end of the stream
        if buf is None:
            break

        # Add the bytes we've read to buf_all.  Note that this
        # technique isn't efficient and shouldn't be used in
        # production code.
        buf_all += buf
        
    assert buf_all == vorbis_file.buffer
    
    
def test_same_data_as_vorbis_file_using_as_array():
    import numpy # type: ignore
    
    # Load the demonstration file that is exactly 5 seconds long
    filename = "../examples/left-right-demo-5s.ogg"

    # Open the file using VorbisFile to read the entire file into memory
    vorbis_file = pyogg.VorbisFile(filename)
    
    # Open the file (again) using VorbisFileStream, which does not read
    # the entire file immediately.
    vorbis_stream = pyogg.VorbisFileStream(filename)

    # Loop through the VorbisFileStream until we've read all the data
    buf_all = None
    while True:
        # Read the next part of the stream
        buf = vorbis_stream.get_buffer_as_array()

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
    assert numpy.all(buf_all == vorbis_file.as_array())
    
