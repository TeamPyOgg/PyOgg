import collections
import copy
import ctypes

from . import opus
from .opus_encoder import OpusEncoder
from .pyogg_error import PyOggError

class OpusBufferedEncoder(OpusEncoder):
    # TODO: This could be made more efficient.  We don't need a
    # deque.  Instead, we need only sufficient PCM storage for one
    # whole packet.  We know the size of the packet thanks to
    # set_frame_size().

    def __init__(self):
        super().__init__()

        self._frame_size_ms = None
        self._frame_size_bytes = None

        # To reduce copying, buffer is a double-ended queue of
        # bytes-objects
        self._buffer = collections.deque()

        # Total number of bytes in the buffer.
        self._buffer_size = 0


    def set_frame_size(self, frame_size):
        """ Set the desired frame duration (in milliseconds).

        Valid options are 2.5, 5, 10, 20, 40, or 60ms.

        """

        # Ensure the frame size is valid.  Compare frame size in
        # units of 0.1ms to avoid floating point comparison
        if int(frame_size*10) not in [25, 50, 100, 200, 400, 600]:
            raise PyOggError(
                "Frame size ({:f}) not one of ".format(frame_size)+
                "the acceptable values"
            )

        self._frame_size_ms = frame_size

        self._calc_frame_size()


    def set_sampling_frequency(self, samples_per_second):
        super().set_sampling_frequency(samples_per_second)
        self._calc_frame_size()


    def encode(self, pcm_bytes, flush=False):
        """Produces Opus-encoded packets from buffered PCM.

        First, pcm_bytes are appended to the end of the internal buffer.

        Then, while there are sufficient bytes in the buffer,
        frames will be encoded.

        This method returns a list, where each item in the list is
        an Opus-encoded frame stored as a bytes-object.

        If insufficient samples are passed in for the specified
        frame size, then an empty list will be returned.

        If flush is set to True, the buffer will be entirely
        emptied and, in the case that there remains PCM for only a
        partial final frame, the PCM will be completed with
        silence to make a complete final frame.

        """
        # Get the encoded packets
        results = self.encode_with_samples(pcm_bytes, flush=flush)

        # Strip the sample lengths
        stripped_results = [encoded_packet for
                            encoded_packet, _ in results]

        return stripped_results

    def encode_with_samples(self, pcm_bytes, flush=False, callback=None):
        """Gets encoded packets and their number of samples.

        This method returns a list, where each item in the list is
        a tuple.  The first item in the tuple is an Opus-encoded
        frame stored as a bytes-object.  The second item in the
        tuple is the number of samples encoded (excluding
        silence).

        If `callback` is supplied then this method will instead
        return an empty list but call the callback for every
        Opus-encoded frame that would have been returned as a
        list.  This option has the desireable property of
        eliminating the copying of the encoded packets, which is
        required in order to form a list.  The callback should
        take two arguments, the encoded frame (a Python bytes
        object) and the number of samples encoded per channel (an
        int).  The user must either process or copy the data as
        the data may be overwritten once the callback terminates.

        """
        self._buffer.append(pcm_bytes)
        self._buffer_size += len(pcm_bytes)

        results = []
        while True:
            # Get PCM from the buffer
            result = self._get_next_frame(add_silence=flush)

            # Check if we've sufficient bytes in the buffer
            if result is None:
                break

            # Separate the components of the result
            pcm_to_encode, samples = result

            # Encode the PCM
            encoded_packet = super().encode(pcm_to_encode)

            if callback is None:
                # Create a deep copy (otherwise the contents will be
                # overwritten if there is a next call to encode
                encoded_packet_copy = copy.deepcopy(encoded_packet)

                # Append the copy of the encoded packet
                results.append((encoded_packet_copy, samples))
            else:
                # Call the callback with the encoded packet; it is
                # the user's responsibility to copy the data if
                # required.
                callback(encoded_packet, samples)

        return results


    def _calc_frame_size(self):
        """Calculates the number of bytes in a frame.

        If the frame size (in milliseconds) and the number of
        samples per seconds have already been specified, then the
        frame size in bytes is set.  Otherwise, this method does
        nothing.

        The frame size is measured in bytes required to store the
        sample.

        """
        if (self._frame_size_ms is None
            or self._samples_per_second is None):
            return

        self._frame_size_bytes = (
            self._frame_size_ms
            * self._samples_per_second
            // 1000
            * ctypes.sizeof(opus.opus_int16)
            * self._channels
        )


    def _get_next_frame(self, add_silence=False):
        """Gets the next Opus-encoded frame.

        Returns a tuple where the first item is the Opus-encoded
        frame and the second item is the number of encoded samples
        (per channel).

        Returns None if insufficient data is available.

        """
        next_frame = bytes()
        samples = 0

        # Ensure frame size has been specified
        if self._frame_size_bytes is None:
            raise PyOggError(
                "Desired frame size hasn't been set.  Perhaps "+
                "encode() was called before set_frame_size() "+
                "and set_sampling_frequency()?"
            )

        # Check if there's insufficient data in the buffer to fill
        # a frame.
        if self._frame_size_bytes > self._buffer_size:
            if len(self._buffer) == 0:
                # No data at all in buffer
                return None
            if add_silence:
                # Get all remaining data
                while len(self._buffer) != 0:
                    next_frame += self._buffer.popleft()
                self._buffer_size = 0
                # Store number of samples (per channel) of actual
                # data
                samples = (
                    len(next_frame)
                    // self._channels
                    // ctypes.sizeof(opus.opus_int16)
                )
                # Fill remainder of frame with silence
                bytes_remaining = self._frame_size_bytes - len(next_frame)
                next_frame += b'\x00' * bytes_remaining
                return (next_frame, samples)
            else:
                # Insufficient data to fill a frame and we're not
                # adding silence
                return None

        bytes_remaining = self._frame_size_bytes
        while bytes_remaining > 0:
            if len(self._buffer[0]) <= bytes_remaining:
                # Take the whole first item
                buffer_ = self._buffer.popleft()
                next_frame += buffer_
                bytes_remaining -= len(buffer_)
                self._buffer_size -= len(buffer_)
            else:
                # Take only part of the buffer

                # TODO: This could be more efficiently
                # implemented.  Rather than appending back the
                # remaining data, we could just update an index
                # saying where we were up to in regards to the
                # first entry of the buffer.
                buffer_ = self._buffer.popleft()
                next_frame += buffer_[:bytes_remaining]
                self._buffer_size -= bytes_remaining
                # And put the unused part back into the buffer
                self._buffer.appendleft(buffer_[bytes_remaining:])
                bytes_remaining = 0

        # Calculate number of samples (per channel)
        samples = (
            len(next_frame)
            // self._channels
            // ctypes.sizeof(opus.opus_int16)
        )

        return (next_frame, samples)
