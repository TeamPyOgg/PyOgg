import wave
from pyogg import OggOpusWriter

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

    # Create an OggOpusWriter
    output_filename = filename+".opus"
    print("Writing OggOpus file to '{:s}'".format(output_filename))
    ogg_opus_writer = OggOpusWriter(output_filename)
    ogg_opus_writer.set_application("audio")
    ogg_opus_writer.set_sampling_frequency(samples_per_second)
    ogg_opus_writer.set_channels(channels)

    # Calculate the desired frame size (in samples per channel)
    desired_frame_duration = 20/1000 # milliseconds
    desired_frame_size = int(desired_frame_duration * samples_per_second)

    # Loop through the wav file's PCM data and encode it as Opus
    while True:
        # Get data from the wav file
        pcm = wave_read.readframes(desired_frame_size)

        # Check if we've finished reading the wav file
        if len(pcm) == 0:
            break

        # Calculate the effective frame size from the number of bytes
        # read
        effective_frame_size = (
            len(pcm) # bytes
            // bytes_per_sample
            // channels
        )

        # Check if we've received enough data
        if effective_frame_size < desired_frame_size:
            # We haven't read a full frame from the wav file, so this
            # is most likely a final partial frame before the end of
            # the file.  We'll pad the end of this frame with silence.
            pcm += (
                b"\x00"
                * ((desired_frame_size - effective_frame_size)
                   * bytes_per_sample
                   * channels)
            )
                
        # Encode the PCM data
        ogg_opus_writer.encode(pcm)
        
    print("Finished.")
