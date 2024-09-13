.. _installation:

Installation
------------

We assume you have both Python and `pip
<https://pip.pypa.io/en/stable/>`_ installed.

Some parts of PyOgg use `NumPy <https://numpy.org/>`_.  Although NumPy
isn't required in order to use PyOgg, it certainly can make things
easier.  To install Numpy::

  pip install numpy

Windows
.......

PyOgg's Wheel distribution for Windows comes with the required DLLs.
Before installing PyOgg, ensure that Python's `Wheel
<https://pypi.org/project/wheel/>`_ package is installed::

  pip install wheel

Then you can install PyOgg::

  pip install pyogg


macOS
.....

A Wheel distribution for PyOgg under macOS is a `work-in-progress
<https://github.com/Zuzu-Typ/PyOgg/issues/32>`_.  However, it is very
easy to install the required libraries using Homebrew.

First, ensure Homebrew itself is installed.  To install Homebrew,
follow the instruction found on Homebrew's `home page
<https://brew.sh/>`_ (there is only one step).

With Homebrew installed, you may install all the libraries used by
PyOgg using this command::

  brew install libogg opus opusfile libopusenc libvorbis flac

If using Apple Silicon, you may have to set DYLD_LIBRARY_PATH::

  export DYLD_LIBRARY_PATH=/opt/homebrew/lib
  
Depending on how you wish to use PyOgg, many of these libraries may be
optional.

Next, install PyOgg::

  pip install pyogg

Finally, you may also find useful the command-line tools ``opusenc``,
``opusdec`` and ``opusinfo``.  These tools provide encoding, decoding, and
general information about OggOpus-encoded files.  They may be
installed with the command::

  brew install opus-tools



Linux
.....

Use the appropriate package installer for your Linux platform.  You
may find the following list helpful; it is the list of libraries used
by PyOgg, with links to their GitLab sources, which can be compiled
directly should pre-compiled libraries not be available:

* `Ogg <https://gitlab.xiph.org/xiph/ogg>`__
* `Vorbis <https://gitlab.xiph.org/xiph/vorbis>`__ (which includes the
  vorbis, vorbisfile, and vorbisenc libraries)
* `Opus <https://gitlab.xiph.org/xiph/opus>`__
* `Opusfile <https://gitlab.xiph.org/xiph/opusfile>`__
* `libopusenc <https://gitlab.xiph.org/xiph/libopusenc>`__
* `flac <https://gitlab.xiph.org/xiph/flac>`__

A note on the Opus library installed under `Amazon Linux 2
<https://aws.amazon.com/amazon-linux-2/>`_: Amazon provides an
outdated version of Opus.  We recommend that you compile your own
version (1.3.1 or later) from the source.


