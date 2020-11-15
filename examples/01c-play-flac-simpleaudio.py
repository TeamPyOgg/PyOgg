# This is an example of playing an Ogg FLAC file using PyOgg and
# simpleaudio.
#
# Author: Matthew Walker 2020-09-12
#
# An Ogg FLAC file (a file containing a FLAC stream wrapped inside an
# Ogg container) is loaded using PyOgg's FlacFile class.  This provides
# the entire file in one PCM encoded buffer.  That buffer is converted
# to a NumPy array and then played using simpleaudio.
#
# To run this example you will need to have installed PyOgg, NumPy,
# and simpleaudio.  These can be installed using pip with the command:
#    pip install numpy pyogg simpleaudio
#
# On successful execution of this program, you should hear the audio
# being played and the console will display:
#
# Reading Ogg Flac file...
# 
# Read Ogg Flac file
# Channels:
#    2
# Frequency (samples per second):
#    48000
# Buffer Length (bytes):
#    960000
# Shape of numpy array (number of samples per channel, number of channels):
#    (240000, 2)
# 
# Playing...
# Finished.

import pyogg
import simpleaudio # type: ignore


# Specify the filename to read
filename = "left-right-demo-5s.flac"

# Read the file using FlacFile
print("Reading Ogg Flac file...")
flac_file = pyogg.FlacFile(filename)

# Display summary information about the audio
print("\nRead Ogg Flac file")
print("Channels:\n  ", flac_file.channels)
print("Frequency (samples per second):\n  ",flac_file.frequency)
print("Buffer Length (bytes):\n  ", len(flac_file.buffer))

# Get the data as a NumPy array
buf = flac_file.as_array()

# The shape of the array can be read as
# "(number of samples per channel, number of channels)".
print(
    "Shape of numpy array (number of samples per channel, "+
    "number of channels):\n  ",
    buf.shape
)

# Play the audio
print("\nPlaying...")
play_obj = simpleaudio.play_buffer(
    buf,
    flac_file.channels,
    flac_file.bytes_per_sample,
    flac_file.frequency
)

# Wait until sound has finished playing
play_obj.wait_done()  

print("Finished.")
