Opus-Related API
================

.. currentmodule:: pyogg

OpusFile
--------
                   
To read an entire OggOpus-encoded audio file into memory, use the
``OpusFile`` class.  For a basic example of its use see
:ref:`getting_started`.  For a more elaborate example see
:ref:`example_play_oggopus`.

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
      
.. autoclass:: OpusFileStream
   :members:
   :undoc-members:
   :inherited-members:

OggOpusWriter
-------------
      
To write OggOpus encoded files, use the ``OggOpusWriter`` class.

.. autoclass:: OggOpusWriter
   :members:
   :undoc-members:
   :inherited-members:
   :special-members: __init__

OpusEncoder
-----------
                     
.. autoclass:: OpusEncoder
   :members:
   :undoc-members:
   :inherited-members:

OpusBufferedEncoder
-------------------
      
.. autoclass:: OpusBufferedEncoder
   :members:
   :undoc-members:
   :inherited-members:

OpusDecoder
-----------
      
.. autoclass:: OpusDecoder
   :members:
   :undoc-members:
   :inherited-members:

