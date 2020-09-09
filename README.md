# PyOgg

PyOgg provides Python bindings for Xiph.org’s Opus, Vorbis and FLAC
audio file formats as well as their Ogg container format.

PyOgg:

- Reads and streams Opus, Vorbis, and FLAC audio formats in their
  standard file format (that is, from within Ogg containers).

- Writes Opus files (that it, Opus-formatted packets into Ogg
  containers)

- Reads and writes Opus-formatted packets (transported, for example,
  via UDP)

Further, should you wish to have still lower-level access, PyOgg
provides ctypes interfaces that give direct access to the C functions
and datatypes found in the libraries.

Under Windows, PyOgg comes bundled with the required dynamic libraries
(DLLs) in the Windows Wheel distributions.

Under macOS, the required libraries can be easily installed using
Homebrew.

PyOgg is not capable of playing audio, however, you can use Python
audio libraries such as simpleaudio, sounddevice, or PyOpenAL to play
audio. PyOpenAL even offers 3D playback.

For more detail, including installation instructions, read the manual
at ____.


Building the Docs
=================

If you are unable to find the documentation at the previously
mentioned address, you may build the documentation yourself.  First,
clone this repository and from within the repository's directory,
install PyOgg in editable mode using::

    pip install -e .
      
Building the documentation requires Sphinx.  To install Sphinx:

    pip install sphinx

Then, enter the `docs` directory and run:

    make html

This will produce a `docs/_build/html` directory.  Open the file
`index.html` to browse the documentation.
