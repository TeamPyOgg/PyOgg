import numpy
import pyogg

filename = "left-right-demo-5s.opus"
opus_file = pyogg.OpusFile(filename)

pcm = opus_file.as_array()
duration_seconds = pcm.shape[0] / opus_file.frequency
print("Audio duration (seconds):", duration_seconds)
