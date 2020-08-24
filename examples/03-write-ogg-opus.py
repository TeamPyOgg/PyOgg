import wave
import pyogg

if __name__ == "__main__":
    # Read a wav file to obtain PCM data
    #filename = "left-right-demo-5s.wav"
    filename = "psallite.opus.wav"
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

    # Create an OggOpusWriter
    output_filename = filename+".opus"
    print("Writing OggOpus file to '{:s}'".format(output_filename))
    ogg_opus_writer = pyogg.OggOpusWriter(output_filename)
    ogg_opus_writer.set_application("audio")
    ogg_opus_writer.set_sampling_frequency(samples_per_second)
    ogg_opus_writer.set_channels(channels)
    ogg_opus_writer.set_frame_size(20) # milliseconds

    # Calculate the desired frame size (in samples per channel)
    desired_frame_duration = 20/1000 # milliseconds
    desired_frame_size = int(desired_frame_duration * samples_per_second)


    # # DEBUG Test zero-length audio file
    # ogg_opus_writer.encode(b"")
    # ogg_opus_writer.close()
    # exit()

    # # DEBUG Test with one 20ms sample
    # sample_length_s = 20 / 1000
    # samples_per_second = 48000
    # sample_length = int(
    #     samples_per_second
    #     * sample_length_s
    #     * channels
    #     * 2 # (size of int16)
    # )
    # sample = b"\x00" * sample_length
    # ogg_opus_writer.encode(sample)
    # ogg_opus_writer.close()
    # exit()

    
    # # DEBUG Test with one sample of length 1
    # sample_length = int(
    #     1
    #     * channels
    #     * 2 # (size of int16)
    # )
    # sample = b"\x00" * sample_length
    # for _ in range(100000):
    #     ogg_opus_writer.encode(sample)
    # ogg_opus_writer.close()
    # exit()


    # # DEBUG Test many samples
    # sample_length_s = 15 / 1000
    # samples_per_second = 48000
    # sample_length = int(
    #     samples_per_second
    #     * sample_length_s
    #     * channels
    #     * 2 # (size of int16)
    # )
    # sample = b"\x00" * sample_length
    # for _ in range(1):
    #     print(f"In 'main': calling OggOpusWriter.encode with sample of {sample_length_s:0.3f} seconds")
    #     ogg_opus_writer.encode(sample)
    # print("In 'main: calling OggOpusWriter.close()")
    # ogg_opus_writer.close()
    # exit()

    
    # Loop through the wav file's PCM data and encode it as Opus
    while True:
        # Get data from the wav file
        pcm = wave_read.readframes(1000)#desired_frame_size)

        # Check if we've finished reading the wav file
        if len(pcm) == 0:
            break

        # # Calculate the effective frame size from the number of bytes
        # # read
        # effective_frame_size = (
        #     len(pcm) # bytes
        #     // bytes_per_sample
        #     // channels
        # )

        # # Check if we've received enough data
        # if effective_frame_size < desired_frame_size:
        #     # We haven't read a full frame from the wav file, so this
        #     # is most likely a final partial frame before the end of
        #     # the file.  We'll pad the end of this frame with silence.
        #     pcm += (
        #         b"\x00"
        #         * ((desired_frame_size - effective_frame_size)
        #            * bytes_per_sample
        #            * channels)
        #     )
                
        # Encode the PCM data
        print("len(pcm):", len(pcm))
        ogg_opus_writer.encode(pcm)

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
