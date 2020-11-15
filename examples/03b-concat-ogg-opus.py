import pyogg

# Read the first file
filename_1 = "left-demo-1s.opus"
file_1 = pyogg.OpusFile(filename_1)

# Read the second file
filename_2 = "right-demo-1s.opus"
file_2 = pyogg.OpusFile(filename_2)

# Create a buffered encoder
encoder = pyogg.OpusBufferedEncoder()
encoder.set_application("audio")
encoder.set_sampling_frequency(48000)
encoder.set_channels(2)
encoder.set_frame_size(20) # milliseconds

# Open a third file for writing.  This will hold the concatenated
# audio of the two files.
filename_out = "output-concat.opus"
file_out = pyogg.OggOpusWriter(filename_out, encoder)

# Pass the data from the first file to the writer
file_out.write(file_1.buffer)

# Pass the data from the second file to the writer
file_out.write(file_2.buffer)

# Close the file (or delete the reference to file_out, which will
# automatically close the file for you).
file_out.close()

print("Finished")
