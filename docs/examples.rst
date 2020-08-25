.. _examples:

Examples
========

The following examples can be found in the `examples directory of the
PyOgg GitHub repository
<https://github.com/Zuzu-Typ/PyOgg/tree/master/examples>`__.

You can run these examples either by downloading the appropriate
file(s) or cloning the repository.  Note that some examples assume
that the demonstration `wave
<https://github.com/Zuzu-Typ/PyOgg/blob/master/examples/left-right-demo-5s.wav?raw=true>`_
and `Opus
<https://github.com/Zuzu-Typ/PyOgg/blob/master/examples/left-right-demo-5s.opus?raw=true>`_
files are available.

.. _example_play_oggopus:

Play an OggOpus file
--------------------

.. literalinclude:: ../examples/01-play-opus-simpleaudio.py

                    
.. _example_opus_file_stream:

Stream an OggOpus file
----------------------

.. literalinclude:: ../examples/04-opus-file-stream.py

                    
.. _example_encode_opus:
                    
Encode and Decode Opus-Packets
------------------------------

.. literalinclude:: ../examples/02-encode-opus.py

                    
.. _example_buffered_encode_opus:
   
Buffered-Encode and Decode Opus-Packets
---------------------------------------

.. literalinclude:: ../examples/02b-buffered-encode-opus.py


Write an OggOpus File
---------------------

.. literalinclude:: ../examples/03-write-ogg-opus.py
