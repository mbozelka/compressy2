# compressy2
A cross-platform application built in wxPython for compressing JPEG and PNG images in bulk.

This was built for a fairly specific reason. Images were needed to be exactly a specific size for spec reasons.

It will compress Jpegs to the specified kb (or slightly under), and will optimize PNGs as best it can.

You can also reduce Jpegs by specifying the percentage. It mathematically reduces the size by that percentage based on the current kb size.

You can specify an output folder, otherwise it will compress the images in an optimized folder within the directory the image currently exists, and you can drag images from multiply folders (or drag entire folders).

NOTE: This will likely not be maintained

## Build
requirements.txt lists the required Python packages needed

setup.py is configured to compile for MacOsx or Windows platforms

To build run
```
python setup.py py2app
```
