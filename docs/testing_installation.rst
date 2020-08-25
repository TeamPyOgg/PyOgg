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
