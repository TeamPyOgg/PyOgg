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


Documentation
-------------

This documentation is built using Sphinx.  To install it::

  pip install sphinx

To build the documentation run::

  cd docs
  make html

You will then find the latest documentation at
``docs/_build/html/index.html``.
