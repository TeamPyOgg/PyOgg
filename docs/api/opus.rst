Opus-Related API
================

The following classes depend on the availability of libraries.

If the required libraries are available then the classes can be
imported directly from the ``pyogg`` module, for example using the
statement ``from pyogg import OpusFile``.  Or you may import the
package using ``import pyogg`` and reference the classes explicitly,
such as ``pyogg.OpusFile``.

If the required libraries are not available then instantiating a class
will raise a ``PyOggError`` exception.


OpusFile
--------
                   
To read an entire OggOpus-encoded audio file into memory, use the
``OpusFile`` class.  For a basic example of its use see
:ref:`getting_started`.  For a more elaborate example see
:ref:`example_play_oggopus`.

This class requires the shared libraries Ogg, Opus, and Opusfile.

.. currentmodule:: pyogg.opus_file
.. autoclass:: OpusFile
   :members:
   :undoc-members:

OpusFileStream
--------------
      
Often, reading an entire file into memory is not desirable.  Rather,
we prefer to stream the file by reading small chunks at a time,
processing the small section of the PCM and then moving on to the next
section.  This can be achieved with the ``OpusFileStream`` class.  For
an example of its use see :ref:`example_opus_file_stream`.

This class requires the shared libraries Ogg, Opus, and Opusfile.

.. currentmodule:: pyogg.opus_file_stream
.. autoclass:: OpusFileStream
   :members:
   :undoc-members:
   :inherited-members:

OggOpusWriter
-------------
      
To write OggOpus encoded files, use the ``OggOpusWriter`` class.

This class requires the shared libraries Ogg and Opus.

.. currentmodule:: pyogg.ogg_opus_writer
.. autoclass:: OggOpusWriter
   :members:
   :undoc-members:
   :inherited-members:
   :special-members: __init__

OpusEncoder
-----------
                     
.. currentmodule:: pyogg.opus_encoder
.. autoclass:: OpusEncoder
   :members:
   :undoc-members:
   :inherited-members:

OpusBufferedEncoder
-------------------
      
.. currentmodule:: pyogg.opus_buffered_encoder
.. autoclass:: OpusBufferedEncoder
   :members:
   :undoc-members:
   :inherited-members:

OpusDecoder
-----------
      
.. currentmodule:: pyogg.opus_decoder
.. autoclass:: OpusDecoder
   :members:
   :undoc-members:
   :inherited-members:

