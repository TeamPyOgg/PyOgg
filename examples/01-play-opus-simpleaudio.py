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
#    $ python 01-play-opus-simpleaudio.py
#    Reading Ogg Opus file...
#    
#    Read Ogg Opus file
#    Channels:
#       2
#    Frequency (samples per second):
#       48000
#    Buffer Length (bytes):
#       960000
#    Shape of numpy array (number of samples per channel, number of channels):
#       (240000, 2)
#    
#    Playing...
#    Finished.


try:
    import pyogg
    import simpleaudio as sa
    import numpy
except ImportError:
    import os
    should_install_requirements = input(\
        "This example requires additional libraries to work.\n" +
        "  py-simple-audio (simpleaudio),\n" +
        "  NumPy (numpy)\n" +
        "  And PyOgg or course.\n" +
        "Would you like to install them right now?\n"+
        "(Y/N): ")
    if should_install_requirements.lower() == "y":
        import subprocess, sys
        
        install_command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            os.path.realpath("01-play-opus-simpleaudio.requirements.txt")
        ]

        popen = subprocess.Popen(install_command,
                                 stdout=subprocess.PIPE, universal_newlines=True)
        
        for stdout_line in iter(popen.stdout.readline, ""):
            print(stdout_line, end="")
            
        popen.stdout.close()
        
        popen.wait()

        print("Done.\n")

        import pyogg
        import simpleaudio as sa
        import numpy

    else:
        os._exit(0)
        
import ctypes
from datetime import datetime


# Specify the filename to read
filename = "left-right-demo-5s.opus"

# Read the file using OpusFile
print("Reading Ogg Opus file...")
opus_file = pyogg.OpusFile(filename)

# Display summary information about the audio
print("\nRead Ogg Opus file")
print("Channels:\n  ", opus_file.channels)
print("Frequency (samples per second):\n  ",opus_file.frequency)
print("Buffer Length (bytes):\n  ", len(opus_file.buffer))

# Get the data as a NumPy array
buf = opus_file.as_array()

# The shape of the array can be read as
# "(number of samples per channel, number of channels)".
print(
    "Shape of numpy array (number of samples per channel, "+
    "number of channels):\n  ",
    buf.shape
)

# Play the audio
print("\nPlaying...")
play_obj = sa.play_buffer(buf,
                          opus_file.channels,
                          opus_file.bytes_per_sample,
                          opus_file.frequency)

# Wait until sound has finished playing
play_obj.wait_done()  

print("Finished.")
