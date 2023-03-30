FaceCropper
Tool for cropping and resizing portrait photos. It is a command line tool that takes a directory of photos and crops them to a square, then resizes them to a specified size. It is written in Python and uses the Pillow library.
Usage: facecropper.py [-h] [-s SIZE] [-o OUTPUT] [-v] directory
positional arguments:  directory   Directory containing photos to crop
-h, --help   show this help message and exit  -s SIZE, --size SIZE   Size to resize cropped photos to (default: 256)  -o OUTPUT, --output OUTPUT   Directory to output cropped photos to (default: cropped)  -v, --verbose   Verbose output
FaceCropper is licensed under the MIT License.

