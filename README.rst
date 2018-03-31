=====
PyOgg
=====

PyOgg provides bindings for Xiph.org's OGG Vorbis, OGG Opus and FLAC audio file formats.

It comes bundled with the required dynamic libraries (.dll) in the Windows WHEEL (.whl) distributions.

The required libraries include the OGG library (e.g. libogg.dll) and at least either OGG Opus' libraries (e.g. libopus.dll, libopusfile.dll) and / or OGG Vorbis' libraries (e.g. libvorbis.dll, libvorbisfile.dll) 
to support Opus and Vorbis respectively, or the FLAC C library (e.g. libFLAC.dll) for FLAC support.

All the functions, structures and datatypes are the same as in the C++ implementation, except for some that couldn't be translated.
If you want to use them natively you will have to use ctypes' data types.
Please refer to the official documentation and the C++ headers.

You can import the various functions from pyogg.ogg, pyogg.vorbis, pyogg.opus and pyogg.flac or use the predefined classes and functions from pyogg.

PyOgg is not capable of playing files, however, you can use OpenAL for normal or even 3D playback with `PyOpenAL <https://pypi.org/project/PyOpenAL>`_.

Currently FLAC cannot be streamed (at least not on Windows), because there seems to be an issue with processing single audio frames.

You can find a reference on `GitHub <https://github.com/Zuzu-Typ/PyOgg>`_
