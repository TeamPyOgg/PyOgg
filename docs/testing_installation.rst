Testing the Installation
========================

A very quick check, to ensure that your newly installed PyOgg package
is working, is to start Python and type ``import pyogg``.  You should
not see any errors::

  $ python
  Python 3.8.5 (default, Jul 21 2020, 10:41:41) 
  [Clang 10.0.0 (clang-1000.11.45.5)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import pyogg
  >>>

You can further test that PyOgg was able to find required libraries.
For example, let's test that PyOgg was able to locate and load the Ogg
library correctly::

  >>> pyogg.PYOGG_OGG_AVAIL
  True

If PyOgg can also locate the Opus and OpusFile libraries, you are
ready to move on to :ref:`getting_started`::

  >>> pyogg.PYOGG_OPUS_AVAIL
  True
  >>> pyogg.PYOGG_OPUS_FILE_AVAIL
  True

If you find that PyOgg is having difficulty finding the shared
libraries, please run the file ``00-test-library-availability.py``
(found in the examples directory of the project's repository):

.. code-block:: text

  python 00-test-library-availability.py

The output shows which libraries were found and, depending on your
platform, where those libraries were found.  This information can be
useful when trying to debug shared-library issues.  Below is an
example of possible output::

  $ python 00-test-library-availability.py 
  Testing the availability of libraries used by PyOgg.
  
  If there are libraries that are not available, PyOgg's abilities will
  be limited.
  
  All libraries used by PyOgg were available.
  
  The libraries that were loaded were found in the following file names:
   - Ogg: /usr/local/lib/libogg.dylib
   - Vorbis: /usr/local/lib/libvorbis.dylib
   - VorbisFile: /usr/local/lib/libvorbisfile.dylib
   - VorbisEnc: /usr/local/lib/libvorbisenc.dylib
   - Opus: /usr/local/lib/libopus.dylib
   - OpusFile: /usr/local/lib/libopusfile.dylib
   - OpusEnc: /usr/local/lib/libopusenc.dylib
   - Flac: /usr/local/lib/libFLAC.dylib
  
  In Linux, from Python version 3.6, the value of the environment variable
  LD_LIBRARY_PATH is used when searching for libraries, if a library cannot
  be found by any other means.
  
  For more information on the process used to locate shared libraries, see
  https://docs.python.org/3/library/ctypes.html#finding-shared-libraries
