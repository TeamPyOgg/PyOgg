.. PyOgg documentation master file, created by
   sphinx-quickstart on Tue Aug 25 10:52:37 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyOgg - Python Bindings for Ogg, Opus, Vorbis and FLAC
======================================================

PyOgg provides Python bindings for Xiph.org's
`Opus <https://www.opus-codec.org/>`_,
`Vorbis <https://xiph.org/vorbis/>`_
and `FLAC <https://xiph.org/flac/>`_
audio file formats as well as their
`Ogg <https://www.xiph.org/ogg/>`_ container format.

PyOgg:

* Reads and streams Opus, Vorbis, and FLAC audio formats in their
  standard file format (that is, from within Ogg containers).
* Writes Opus files (that it, Opus-formatted packets into Ogg
  containers)
* Reads and writes Opus-formatted packets (transported, for example,
  via UDP)

Further, should you wish to have still lower-level access, PyOgg
provides `ctypes <https://docs.python.org/3/library/ctypes.html>`_
interfaces that give direct access to the C functions and datatypes
found in the libraries.
  
Under Windows, PyOgg comes bundled with the required dynamic libraries
(DLLs) in the Windows Wheel distributions.

Under macOS, the required libraries can be easily installed using
`Homebrew <https://brew.sh/>`_.

PyOgg is not capable of playing audio, however, you can use Python
audio libraries such as `simpleaudio
<https://pypi.org/project/simpleaudio/>`_, `sounddevice
<https://pypi.org/project/sounddevice/>`_, or `PyOpenAL
<https://pypi.org/project/PyOpenAL/>`_ to play audio.  PyOpenAL even
offers 3D playback.

----


.. toctree::
             
   installation
   testing_installation
   getting_started
   examples
   api/index
             
* :ref:`genindex`
