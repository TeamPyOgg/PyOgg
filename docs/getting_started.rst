.. _getting_started:

Getting Started
---------------

To get started with PyOgg, make sure you've followed the installation
instructions (see :ref:`installation`).  The next section gives a very
easy introduction for a first project with PyOgg.

First Project
.............

As a first project, let's create a program that outputs the duration
of an Opus-encoded audio file.

We'll make it easy for ourselves and use `NumPy
<https://numpy.org/>`_.  Make sure you've installed it.  To install
NumPy run the command::

  pip install numpy

Next, create a directory (folder) to save our work.

Download the `example OggOpus file
<https://github.com/Zuzu-Typ/PyOgg/blob/master/examples/left-right-demo-5s.opus?raw=true>`_
and save it as ``left-right-demo-5s.opus`` in the directory you just
created.  This file is *exactly* five seconds long.

Create a Python program in your favourite editor, let's call the file
``getting_started.py``.

As the first lines of your file, Import the PyOgg and NumPy libraries with the
lines::

  import numpy
  import pyogg
  

We'll now use the PyOgg class ``OpusFile`` to read the example OggOpus
file into memory::

  filename = "left-right-demo-5s.opus"
  opus_file = pyogg.OpusFile(filename)

The contents of the file, stored in `PCM
<https://en.wikipedia.org/wiki/Pulse-code_modulation>`_ can now be
obtained using the method ``as_array()``.

The method returns a NumPy array containing all the audio in the file.
NumPy provides a ``shape`` attribute that gives us the size of the
array.  In our case, this will give us ``(240000,2)``.  What do these
numbers mean?

The second number in the tuple is easy to understand: the ``2`` tells
us there are two channels, thus this file is in stereo.

But what about the first number, the 240,000?  That's the number of
samples per channel.  The quality of an audio recording is partially
governed by the number of samples recorded per second.  Opus-encoded
recordings are typically saved at 48,000 samples per second.  We can
get this number from ``opus_file.frequency``.

Now we have enough information to calculate the duration of the audio::

  pcm = opus_file.as_array()
  duration_seconds = pcm.shape[0] / opus_file.frequency
  print("Audio duration (seconds):", duration_seconds)

**Note:** If you're not using Python 3, you will have to adapt the ``print``
command by removing the parentheses in that line.
  
Run your Python program from within the directory we created at the
start and you should see something similar to::

  $ python getting_started.py 
  Audio duration (seconds): 5.0  

Below is the complete example:

.. literalinclude:: getting_started.py


Next Steps
..........

To continue learning more about PyOgg, you might like to try running a
few of the example files provided with PyOgg (see :ref:`examples`).
You might like to consider the first example and actually play our
demonstration OggOpus file.

You may also like to jump in and explore the :ref:`api`.
