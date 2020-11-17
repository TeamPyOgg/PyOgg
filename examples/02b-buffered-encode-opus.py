import wave
from pyogg import OpusBufferedEncoder
from pyogg import OpusDecoder

if __name__ == "__main__":
    # Setup encoding
    # ==============
    
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

    # Create an Opus encoder
    opus_encoder = OpusBufferedEncoder()
    opus_encoder.set_application("audio")
    opus_encoder.set_sampling_frequency(samples_per_second)
    opus_encoder.set_channels(channels)
    desired_frame_duration = 20 # ms
    opus_encoder.set_frame_size(desired_frame_duration)

    # Setup decoding
    # ==============

    # Create an Opus decoder
    opus_decoder = OpusDecoder()
    opus_decoder.set_channels(channels)
    opus_decoder.set_sampling_frequency(samples_per_second)

    # Open an output wav for the decoded PCM
    output_filename = "output-"+filename
    wave_write = wave.open(output_filename, "wb")
    print("Writing wav into file '{:s}'".format(output_filename))

    # Save the wav's specification
    wave_write.setnchannels(channels)
    wave_write.setframerate(samples_per_second)
    wave_write.setsampwidth(bytes_per_sample)

    # Execute encode-decode
    # =====================
    
    # Loop through the wav file's PCM data and encode it as Opus
    bytes_encoded = 0
    finished = False
    while not finished:
        # Get data from the wav file
        frames_per_read = 1000
        pcm = wave_read.readframes(frames_per_read)

        # Check if we've finished reading the wav file
        if len(pcm) == 0:
            # Encode what's left of the PCM and flush it by filling
            # any partial frames with silence.
            finished = True

        # Encode the PCM data
        encoded_packets = opus_encoder.buffered_encode(
            memoryview(bytearray(pcm)), # FIXME
            flush=finished
        )

        # At this stage we now have a list of Opus-encoded packets.
        # These could be sent over UDP, for example, and then decoded
        # with OpusDecoder.  However they cannot really be saved to a
        # file without wrapping them in the likes of an Ogg stream;
        # for this see OggOpusWriter.
            
        # For this example, we will now immediately decode the encoded
        # packets using OpusDecoder.
        for encoded_packet, _, _ in encoded_packets:
            bytes_encoded += len(encoded_packet)

            decoded_pcm = opus_decoder.decode(encoded_packet)

            # Save the decoded PCM as a new wav file
            wave_write.writeframes(decoded_pcm)

    wave_read.close()
    wave_write.close()
    print("Total bytes of encoded packets:", bytes_encoded)
    print("Finished.")
