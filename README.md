# PyOgg

PyOgg is a very simple implementation of Xiph.org's OGG audio file type.

It requires libogg.dll and at least either OGG OPUS' libraries (libopus, libopusfile) or OGG VORBIS' libraries (libvorbis, libvorbisfile)

All the functions, structures and datatypes are as in the C++ implementation, except for some that couldn't be translated.

You can import the various functions from pyogg.ogg, pyogg.value and pyogg.opus, or use the predefined VorbisFile and OpusFile classes from pyogg.