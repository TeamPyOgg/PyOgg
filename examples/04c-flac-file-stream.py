"""Reads an Ogg Flac file using FlacFile and FlacFileStream.

Reads an Ogg Flac file using FlacFileStream and compares it to the
results of reading it with FlacFile.  Gives timing information for the
two approaches.

A typical output:

TODO

"""

import time

import numpy
import pyogg

# Specify a file to process
flac_file_filename = "left-right-demo-5s.flac"
flac_file_stream_filename = "left-right-demo-5s.flac"

# Open the file using FlacFile, which reads the entire file
# immediately and places it into an internal buffer.
start_time = time.time()
flac_file = pyogg.FlacFile(flac_file_filename)
end_time = time.time()
duration = (end_time-start_time)*1000
array = flac_file.as_array()
array_index = 0
print("Read {:d} samples from FlacFile (in {:.1f} milliseconds).".format(
    len(array),
    duration
))

# Open the file using FlacFileStream, which does not read the entire
# file immediately.
stream = pyogg.FlacFileStream(flac_file_stream_filename)

# Loop through the FlacFileStream until we've read all the data
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
        print("FlacFileStream data was identical to FlacFile data,\n"+
              "however there was more data in the FlacFileStream than\n"+
              "in the FlacFile.")
        identical = False
        break

    # Compare the stream with the FlacFile data.  (They should be
    # identical.)
    comparison = array[array_index:array_index+len(buf)] == buf
    if not numpy.all(comparison):
        print("FlacFileStream data was NOT identical to FlacFile data.")
        identical = False
        break

    # Move the FlacFile index along
    array_index += len(buf)

avg_time = numpy.mean(times)
print(
    ("Read {:d} samples from the FlacFileStream\n"+
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
    print("FlacFileStream data was identical to FlacFile data.")
else:
    # There was remaining data
    print("FlacFileStream data was identical to FlacFile data,\n"+
          "however there was more data in the FlacFile than\n"+
          "in the FlacFileStream.")
