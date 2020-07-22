import pyogg

print("Testing the availability of libraries used by PyOgg.")
print("")
print("If there are libraries that are not available, PyOgg's abilities will")
print("be limited.\n")

libraries_available = {
    "Ogg": pyogg.PYOGG_OGG_AVAIL,
    "Vorbis": pyogg.PYOGG_VORBIS_AVAIL,
    "VorbisFile": pyogg.PYOGG_VORBIS_FILE_AVAIL,
    "VorbisEnc": pyogg.PYOGG_VORBIS_ENC_AVAIL,
    "Opus": pyogg.PYOGG_OPUS_AVAIL,
    "OpusFile": pyogg.PYOGG_OPUS_FILE_AVAIL,
    "OpusEnc": pyogg.PYOGG_OPUS_ENC_AVAIL,
    "Flac": pyogg.PYOGG_FLAC_AVAIL
}

if all(libraries_available.values()):
    print("All libraries used by PyOgg were available.")

else:
    print("The following libraries were not available:")
    for library_name, available in libraries_available.items():
        if not available:
            print(" - "+library_name)

print("\nThe libraries that were loaded were found in the following file names:")

libraries = {
    "Ogg": pyogg.ogg.libogg,
    "Vorbis": pyogg.vorbis.libvorbis,
    "VorbisFile": pyogg.vorbis.libvorbisfile,
    "VorbisEnc": pyogg.vorbis.libvorbisenc,
    "Opus": pyogg.opus.libopus,
    "OpusFile": pyogg.opus.libopusfile,
    "OpusEnc": pyogg.opus.libopusenc,
    "Flac": pyogg.flac.libflac
}

for library_name, lib in libraries.items():
    filename = "(not loaded)"
    if lib is not None:
        filename = lib._name
    print(" - "+library_name+": "+filename)

print("\nIn Linux, from Python version 3.6, the value of the environment variable")
print("LD_LIBRARY_PATH is used when searching for libraries, if a library cannot")
print("be found by any other means.")
print("")
print("For more information on the process used to locate shared libraries, see")
print("https://docs.python.org/3/library/ctypes.html#finding-shared-libraries")
