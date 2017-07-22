# PyOgg

PyOgg is a very simple implementation of Xiph.org's OGG audio file type.

It requires libogg.dll and at least either OGG OPUS' libraries (libopus, libopusfile) or OGG VORBIS' libraries (libvorbis, libvorbisfile)

All the functions, structures and datatypes are as in the C++ implementation, except for some that couldn't be translated.

In addition to those, there is currently one extra function that takes care of reading OGG VORBIS files.
It is called pyogg_ov_read and takes a OggVorbis_File, a buffer (in form of a bytes string), the size of read buffers (usually 32768), bigendianp, word, sgned 

NOTE: I've just started developing this and there is no support for OGG OPUS yet.