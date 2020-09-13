import os
import platform
from setuptools import setup

# "Import" __version__ from PyOgg's __init__.py.  This allows us to
# query PyOgg's version from within Python too.  For discussion on
# alternative techniques see
# https://packaging.python.org/guides/single-sourcing-package-version/
__version__ = 'unknown'
for line in open('pyogg/__init__.py'):
    if line.startswith('__version__'):
        exec(line)
        break

    
# Eventually we may wish to be specific as to which interpreters we
# support.  This could be done with the following:
# pythons = '.'.join([
#     'cp32', 'cp33', 'cp34', 'cp35', 'cp36', 'cp37', 'cp38', 'cp39',
#     'pp32', 'pp33', 'pp34', 'pp35', 'pp36', 'pp37',
# ])
# However, for the moment, we'll just say the we support all Python 2
# and Python 3 interpreters.  For more information see
# https://www.python.org/dev/peps/pep-0425/#platform-tag
pythons = '.'.join(['py2', 'py3'])


# Environment variables for cross-platform package creation.  Set the
# appropriate environment variable to override the current system's
# value.
system = os.environ.get(
    'PYTHON_PYOGG_PLATFORM',
    platform.system()
)
architecture = os.environ.get(
    'PYTHON_PYOGG_ARCHITECTURE',
    platform.architecture()[0]
)


# Define the shared libraries to include in the Wheel packages.
if system == 'Darwin':
    print("Packaging shared libraries for macOS")
    package_data = {
        'pyogg': ["libs/macos/"+libname for libname in [
            'libogg.0.dylib',
            'libopus.0.dylib',
            'libopusfile.0.dylib',
            'libopusenc.0.dylib',
            'libvorbis.0.dylib',
            'libvorbisfile.3.dylib',
            'libvorbisenc.2.dylib',
            'libFLAC.8.dylib'
        ]]
    }
    zip_safe = False
elif system == 'Windows':
    # This could be made dependent on 32/64-bit architectures, based
    # on the achitecture variable above.
    print("Packaging shared libraries for Windows")
    print("achitecture:", architecture)
    win_dirs = {
        "32bit": "win32",
        "64bit": "win_amd64"
    }
    win_dir = win_dirs[architecture]
    package_data = {
        'pyogg': ["libs/"+win_dir+"/"+libname for libname in [
            'libFLAC.dll',
            'ogg.dll',
            'libvorbis.dll',
            'libvorbisfile.dll',
            'opus.dll',
            'opusenc.dll',
            'opusfile.dll',
            'libssl-1_1-x64.dll',
            'libcrypto-1_1-x64.dll'
        ]]
    }
    zip_safe = False
else:
    print("Unknown system; not packaging any shared libraries")
    package_data = {}
    zip_safe = True


# Override the 'bdist_wheel' command to create OS-dependent byt
# Python-independent wheels
try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    cmdclass = {}
else:
    class bdist_wheel_half_pure(bdist_wheel):
        """Create OS-dependent, but Python-independent wheels."""

        def get_tag(self):
            abi = 'none'
            if system == 'Darwin':
                oses = 'macosx_10_6_x86_64'
            elif system == 'Windows':
                if architecture == '32bit':
                    oses = 'win32'
                else:
                    oses = 'win_amd64'
            else:
                oses = 'any'
            return pythons, abi, oses

    cmdclass = {'bdist_wheel': bdist_wheel_half_pure}
    
setup(
    name='PyOgg',
    version=__version__,
    description="Xiph.org's Ogg Vorbis, Opus and FLAC for Python",
    long_description=open('docs/description.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/Zuzu-Typ/PyOgg',
    author='Zuzu_Typ',
    author_email='zuzu.typ@gmail.com',
    license='BSD 3-clause "New" or "Revised"',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Sound/Audio',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='Xiph ogg vorbis opus flac sound playback audio',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['pyogg'],

    # The shared libraries to include are defined above
    package_data=package_data,
    zip_safe=zip_safe,
    
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.

    # Reference to the command class defined above
    cmdclass=cmdclass,    
)
