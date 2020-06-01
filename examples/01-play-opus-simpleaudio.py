# This is an example of the use of PyOgg.
#
# Author: Matthew Walker 2020-06-01
#
# An Ogg Opus file (a file containing an Opus stream wrapped inside an
# Ogg container) is loaded using the Opusfile library.  This provides
# the entire file in one PCM encoded buffer.  That buffer is converted
# to a NumPy array and then played using simpleaudio.
#
# On successful execution of this program, you should hear the audio
# being played and the console will display comething like:
#
#    Reading Ogg Opus file...
# 
#    Read Ogg Opus file
#    Channels: 2
#    Frequency (samples per second): 48000
#    Buffer Length (bytes): 960000
#    Shape of numpy array (number of samples per channel, number of channels): (240000, 2)
#    
#    Playing...
#    Duration: 0:00:05.190433
#    Finished.


import pyogg
import simpleaudio as sa
import numpy
import ctypes
from datetime import datetime


# Specify the filename to read
filename = "left-right-demo-5s.opus"


# Read the file using OpusFile
print("Reading Ogg Opus file...")
opusFile = pyogg.OpusFile(filename)


# Display summary information about the audio
print("\nRead Ogg Opus file")
print("Channels:", opusFile.channels)
print("Frequency (samples per second):",opusFile.frequency)
print("Buffer Length (bytes):", opusFile.buffer_length)


# Using the data from the buffer in OpusFile, create a NumPy array
# with the correct shape.  Note that this does not copy the buffer's
# data.
bytesPerSample = ctypes.sizeof(opusFile.buffer.contents)
buffer = numpy.ctypeslib.as_array(
    opusFile.buffer,
    (opusFile.buffer_length//
     bytesPerSample//
     opusFile.channels,
     opusFile.channels)
)


# The shape of the array can be read as (number of samples per
# channel, number of channels).
print("Shape of numpy array (number of samples per channel, number of channels):",
      buffer.shape)


# Play the audio
print("\nPlaying...")
startTime = datetime.now()
play_obj = sa.play_buffer(buffer,
                          opusFile.channels,
                          bytesPerSample,
                          opusFile.frequency)


# Wait until sound has finished playing
play_obj.wait_done()  


# Report on the time spent during playback
endTime = datetime.now()
print("Duration: "+str(endTime - startTime))
print("Finished.")
