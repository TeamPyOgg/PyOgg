PyOgg Development
=================

If you are interested in contributing to the development of PyOgg:

* The master git repository can be found on the `project's GitHub site
  <https://github.com/Zuzu-Typ/PyOgg>`_.

* If you would like to report a bug or have a feature request,
  consider posting to an issue on the project's GitHub site.

* Finally, please make a pull request if you develop code you'd like
  to have added into PyOgg.


Editable Install
----------------

If you're developing PyOgg, you may find it more convenient if PyOgg
is installed in editable mode.  From the same directory as
``setup.py`` can be found, run::

  pip install -e .
  

Automated Tests
---------------

PyOgg includes a collection of automated tests.  They require
``pytest``, which can be installed with::

  pip install pytest

**Note:** If you have an old version of pytest installed, make sure to
install an up-to-date version (say, in a virtual environment).  If you
do so, please restart Terminal as you may otherwise encounter spurious
``ModuleNotFoundError`` errors.  For more information, see `Dirk
Avery's blog post on pytest
<https://medium.com/@dirk.avery/pytest-modulenotfounderror-no-module-named-requests-a770e6926ac5>`__
or check your version of pytest by running::

  pytest --version

Once you have pytest installed, you may run the tests with the
commands::

  cd tests
  pytest

This should output something similar to::

  $ pytest
  ========================= test session starts =========================
  platform darwin -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
  rootdir: /Users/matthew/Desktop/VirtualChoir/PyOgg/PyOgg
  collected 39 items                                                    
  
  test_ogg_opus_writer.py ......                                  [ 15%]
  test_opus_buffered_encoder.py ....                              [ 25%]
  test_opus_decoder.py .........                                  [ 48%]
  test_opus_encoder.py ............                               [ 79%]
  test_opus_file.py ....                                          [ 89%]
  test_opus_file_stream.py ....                                   [100%]
  
  ========================= 39 passed in 1.20s ==========================

  
As at August 2020, we had about 75% code coverage.  This can be
examined by installing the Python coverage package::

  pip install coverage

And then running the tests with the command::

  coverage run --source=../pyogg -m pytest
  coverage html

You can then open the file ``htmlcov/index.html``, which gives a
detailed line-by-line analysis of the tests' coverage.


Static Type Checking
--------------------

As at November 2020, a considerable portion of PyOgg has had type
hinting added.  This allows for static type checkers such as
`mypy <http://mypy-lang.org/>`_ to be used, which can help detect bugs,
without even running your code.

Mypy is run as part of the Travis continuous integration script;
checking is performed on both the PyOgg package itself and also its
automated tests.

To run the mypy checks yourself, you will need to have mypy
installed::

  pip install mypy

The tests for the PyOgg package can then by run from the root of the
git repository using::

  mypy -p pyogg

Checking of the automated tests can be done (also from the root of the
repository) with::

  mypy tests/*.py




Documentation
-------------

The documentation is built automatically by Read the Docs everytime
there is an update of the master branch of the git repository.  Thus,
the latest version, and indeed the previous versions, of the
documentation are always available at `Read the Docs
<https://pyogg.readthedocs.io/en/latest/>`_.

Further, the documentation is also built as part of the Travis
continuous integration script.

To build the documentation yourself requires Sphinx.  To install it::

  pip install sphinx

If you are building the documentation under Windows, you may need to
install `Make for Windows
<http://gnuwin32.sourceforge.net/packages/make.htm>`_.

To build the documentation run::

  cd docs
  make html

You will then find the latest documentation at
``docs/_build/html/index.html``.


Building Wheels
---------------

Wheels can be built for macOS, 32-bit Windows and 64-bit Windows.  For
these systems, pre-compiled shared libraries can be found in the
project repository under ``pyogg/libs/``.

To build a Wheel you will need to have installed setuptools and wheel::

  pip install --upgrade setuptools
  pip install --upgrade wheel

By default, the build script will create a Wheel for your current
platform::

  python setup.py build bdist_wheel

If you wish to create a Wheel for a different platform, set the
environment variable ``PYTHON_PYOGG_PLATFORM`` to either ``Darwin``
for a macOS wheel, or ``Windows`` for Microsoft Windows platforms.
For Windows, you will also need to set the environment variable
``PYTHON_PYOGG_ARCHITECTURE`` to either ``32bit`` or ``64bit`` as
required.  Finally, run the same build command list above.

Ensure that the version for your wheel is correct.  The version
definition can be found in ``pyogg/__init__.py``.
