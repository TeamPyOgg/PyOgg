# PyOgg

PyOgg provides bindings for Xiph.org's OGG Vorbis and OGG Opus audio file formats.

It requires libogg.dll and at least either OGG Opus' libraries (libopus.dll, libopusfile.dll) and / or OGG Vorbis' libraries (libvorbis.dll, libvorbisfile.dll) to support Opus and Vorbis respectively.
(PyOgg is technically cross-platform, but it only searches for Windows .DLL files)

All the functions, structures and datatypes are the same as in the C++ implementation, except for some that couldn't be translated.
If you want to use them natively you will have to use ctypes' data types.
Please refer to the official documentation and the C++ headers.

You can import the various functions from pyogg.ogg, pyogg.vorbis and pyogg.opus or use the predefined classes and functions from pyogg.

Here's a reference for PyOgg's own classes and functions:

	<class> pyogg.VorbisFile(path)
		# opens and reads an OGG Vorbis file to a buffer. 
			<str> path # path to the file (can be relative or absolute)
		
		<int> VorbisFile.channels
			# how many audio channels the audio data has (1 = mono, 2 = stereo, etc.)
		
		<int> VorbisFile.frequency
			# audio frequency (e.g. 48000, 44100, etc.)
			
		<str or bytes> VorbisFile.buffer
			# audio data
			
		<int> VorbisFile.buffer_length
			# length of the buffer
			
	<class> pyogg.OpusFile(path)
		# opens and reads an OGG Opus file to a buffer. 
			<str> path # path to the file (can be relative or absolute)
		
		<int> OpusFile.channels
			# how many audio channels the audio data has (1 = mono, 2 = stereo, etc.)
		
		<int> OpusFile.frequency
			# audio frequency (always 48000)
			
		<opus_int16_p> OpusFile.buffer
			# audio data
			
		<int> OpusFile.buffer_length
			# length of the buffer
			
	<class> pyogg.VorbisFileStream(path)
		# opens an OGG Vorbis file and prepares it for repeated reading. 
			<str> path # path to the file (can be relative or absolute)
			
		<vorbis.OggVorbis_File> VorbisFileStream.vf
			# Vorbis audio file stream
			
		<int> VorbisFileStream.channels
			# how many audio channels the audio data has (1 = mono, 2 = stereo, etc.)
		
		<int> VorbisFileStream.frequency
			# audio frequency (always 48000)
			
		<method> get_buffer() -> [buffer, buffer_length] or None
			# reads some audio data into a buffer (to set the buffer size, see pyoggSetStreamBufferSize)
			# if the file reaches it's end this method returns None
				<str or bytes> buffer # a buffer containing some audio data
				<int> buffer_length   # length of the buffer
				
		<method> clean_up() -> None
			# deletes the buffer and closes the file
			
	<class> pyogg.OpusFileStream(path)
		# opens an OGG Opus file and prepares it for repeated reading. 
			<str> path # path to the file (can be relative or absolute)
			
		<vorbis.OggVorbis_File> OpusFileStream.vf
			# Opus audio file stream
			
		<int> OpusFileStream.channels
			# how many audio channels the audio data has (1 = mono, 2 = stereo, etc.)
		
		<int> OpusFileStream.frequency
			# audio frequency (always 48000)
			
		<method> get_buffer() -> [buffer, buffer_length] or None
			# reads some audio data into a buffer (to set the buffer size, see pyoggSetStreamBufferSize)
			# if the file reaches it's end this method returns None
				<opus_int16_p> buffer # a buffer containing some audio data
				<int> buffer_length   # length of the buffer
				
		<method> clean_up() -> None
			# deletes the buffer and closes the file
			
	<method> pyogg.pyoggSetStreamBufferSize(size)
		# changes the maximum size for stream buffers (initially 8192)
			<int> size # how much data each stream buffer holds
			
