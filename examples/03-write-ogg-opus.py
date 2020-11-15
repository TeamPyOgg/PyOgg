import wave
import pyogg

if __name__ == "__main__":
    # Read a wav file to obtain PCM data
    filename = "left-right-demo-5s.wav"
    wave_read = wave.open(filename, "rb")
    print("Reading wav from file '{:s}'".format(filename))

    # Extract the wav's specification
    channels = wave_read.getnchannels()
    print("Number of channels:", channels)
    samples_per_second = wave_read.getframerate()
    print("Sampling frequency:", samples_per_second)
    bytes_per_sample = wave_read.getsampwidth()
    original_length = wave_read.getnframes()
    print("Length:", original_length)

    # Create a OpusBufferedEncoder
    opus_buffered_encoder = pyogg.OpusBufferedEncoder()
    opus_buffered_encoder.set_application("audio")
    opus_buffered_encoder.set_sampling_frequency(samples_per_second)
    opus_buffered_encoder.set_channels(channels)
    opus_buffered_encoder.set_frame_size(20) # milliseconds
    
    # Create an OggOpusWriter
    output_filename = filename+".opus"
    print("Writing OggOpus file to '{:s}'".format(output_filename))
    ogg_opus_writer = pyogg.OggOpusWriter(
        output_filename,
        opus_buffered_encoder
    )

    # Calculate the desired frame size (in samples per channel)
    desired_frame_duration = 20/1000 # milliseconds
    desired_frame_size = int(desired_frame_duration * samples_per_second)
    
    # Loop through the wav file's PCM data and write it as OggOpus
    chunk_size = 1000 # bytes
    while True:
        # Get data from the wav file
        pcm = wave_read.readframes(chunk_size)

        # Check if we've finished reading the wav file
        if len(pcm) == 0:
            break

        # Encode the PCM data
        ogg_opus_writer.write(
            memoryview(bytearray(pcm)) # FIXME
        )

    # We've finished writing the file
    ogg_opus_writer.close()

    # Check that the output file is that same length as the original
    print("Reading output file:", output_filename)
    opus_file = pyogg.OpusFile(output_filename)
    print("File read")
    output_length = opus_file.as_array().shape[0]
    print("Output length:", output_length)

    if original_length != output_length:
        print("ERROR: The original length is different to the output length")
        
    print("Finished.")
