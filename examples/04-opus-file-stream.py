"""Reads an Ogg-Opus file using OpusFile and OpusFileStream.

Reads an Ogg-Opus file using OpusFileStream and compares it to the
results of reading it with OpusFile.  Gives timing information for the
two approaches.

A typical output:

Read 240000 samples from OpusFile (in 53.8 milliseconds).
Read 240000 samples from the OpusFileStream
(in 252 reads averaging 0.23 milliseconds each).
OpusFileStream data was identical to OpusFile data.

"""

import time

import numpy
import pyogg

# Specify a file to process
opus_file_filename = "left-right-demo-5s.opus"
opus_file_stream_filename = "left-right-demo-5s.opus"

# Open the file using OpusFile, which reads the entire file
# immediately and places it into an internal buffer.
start_time = time.time()
opus_file = pyogg.OpusFile(opus_file_filename)
end_time = time.time()
duration = (end_time-start_time)*1000
array = opus_file.as_array()
array_index = 0
print("Read {:d} samples from OpusFile (in {:.1f} milliseconds).".format(
    len(array),
    duration
))

# Open the file using OpusFileStream, which does not read the entire
# file immediately.
stream = pyogg.OpusFileStream(opus_file_stream_filename)

# Loop through the OpusFileStream until we've read all the data
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
        print("OpusFileStream data was identical to OpusFile data,\n"+
              "however there was more data in the OpusFileStream than\n"+
              "in the OpusFile.")
        identical = False
        break

    # Compare the stream with the OpusFile data.  (They should be
    # identical.)
    comparison = array[array_index:array_index+len(buf)] == buf
    if not numpy.all(comparison):
        print("OpusFileStream data was NOT identical to OpusFile data.")
        identical = False
        break

    # Move the OpusFile index along
    array_index += len(buf)

avg_time = numpy.mean(times)
print(
    ("Read {:d} samples from the OpusFileStream\n"+
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
    print("OpusFileStream data was identical to OpusFile data.")
else:
    # There was remaining data
    print("OpusFileStream data was identical to OpusFile data,\n"+
          "however there was more data in the OpusFile than\n"+
          "in the OpusFileStream.")
