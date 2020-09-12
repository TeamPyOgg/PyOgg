"""Reads an Ogg Vorbis file using VorbisFile and VorbisFileStream.

Reads an Ogg Vorbis file using VorbisFileStream and compares it to the
results of reading it with VorbisFile.  Gives timing information for the
two approaches.

A typical output:

TODO

"""

import time

import numpy
import pyogg

# Specify a file to process
vorbis_file_filename = "left-right-demo-5s.ogg"
vorbis_file_stream_filename = "left-right-demo-5s.ogg"

# Open the file using VorbisFile, which reads the entire file
# immediately and places it into an internal buffer.
start_time = time.time()
vorbis_file = pyogg.VorbisFile(vorbis_file_filename)
end_time = time.time()
duration = (end_time-start_time)*1000
array = vorbis_file.as_array()
array_index = 0
print("Read {:d} samples from VorbisFile (in {:.1f} milliseconds).".format(
    len(array),
    duration
))

# Open the file using VorbisFileStream, which does not read the entire
# file immediately.
stream = pyogg.VorbisFileStream(vorbis_file_stream_filename)

# Loop through the VorbisFileStream until we've read all the data
samples_read = 0
identical = True
times = []
while True:
    # Read the next part of the stream
    start_time = time.time()
    buf = stream.get_buffer_as_array()
    end_time = time.time()
    duration = (end_time-start_time)*1000
    times.append(duration)

    # Check if we've reached the end of the stream
    if buf is None:
        break

    # Increment the number of samples read
    samples_read += len(buf)

    # Check we've not read too much data from the stream
    if array_index+len(buf) > len(array):
        print("VorbisFileStream data was identical to VorbisFile data,\n"+
              "however there was more data in the VorbisFileStream than\n"+
              "in the VorbisFile.")
        identical = False
        break

    # Compare the stream with the VorbisFile data.  (They should be
    # identical.)
    comparison = array[array_index:array_index+len(buf)] == buf
    if not numpy.all(comparison):
        print("VorbisFileStream data was NOT identical to VorbisFile data.")
        identical = False
        break

    # Move the VorbisFile index along
    array_index += len(buf)

avg_time = numpy.mean(times)
print(
    ("Read {:d} samples from the VorbisFileStream\n"+
     "(in {:d} reads averaging {:.2f} milliseconds each).").format(
         samples_read,
         len(times),
         avg_time
     )
)

if identical == False:
    # We've finished our work here
    pass
elif array_index == len(array):
    # We completed the comparison successfully.
    print("VorbisFileStream data was identical to VorbisFile data.")
else:
    # There was remaining data
    print("VorbisFileStream data was identical to VorbisFile data,\n"+
          "however there was more data in the VorbisFile than\n"+
          "in the VorbisFileStream.")
