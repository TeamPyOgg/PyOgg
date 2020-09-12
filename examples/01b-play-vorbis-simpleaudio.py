# This is an example of playing an Ogg Vorbis file using PyOgg and
# simpleaudio.
#
# Author: Matthew Walker 2020-09-12
#
# An Ogg Vorbis file (a file containing a Vorbis stream wrapped inside an
# Ogg container) is loaded using PyOgg's VorbisFile class.  This provides
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
# Reading Ogg Vorbis file...
# 
# Read Ogg Vorbis file
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
import simpleaudio


# Specify the filename to read
filename = "left-right-demo-5s.ogg"

# Read the file using VorbisFile
print("Reading Ogg Vorbis file...")
vorbis_file = pyogg.VorbisFile(filename)

# Display summary information about the audio
print("\nRead Ogg Vorbis file")
print("Channels:\n  ", vorbis_file.channels)
print("Frequency (samples per second):\n  ",vorbis_file.frequency)
print("Buffer Length (bytes):\n  ", len(vorbis_file.buffer))

# Get the data as a NumPy array
buf = vorbis_file.as_array()

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
    vorbis_file.channels,
    vorbis_file.bytes_per_sample,
    vorbis_file.frequency
)

# Wait until sound has finished playing
play_obj.wait_done()  

print("Finished.")
