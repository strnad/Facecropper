# Facecropper - Face Cropping App

This face cropping app detects faces in images and crops them based on the provided parameters. It is a command-line tool that takes input images from a folder, processes them, and saves the cropped images in the output folder. The app can be run with default parameters or interactively, allowing users to customize the parameters.

## Prerequisites

- Python 3.6 or later

## Installation

1. Clone this repository to your local machine or download and extract the zip file.
2. Open a terminal window and navigate to the repository folder.
3. Run the 'install.bat' script to set up the virtual environment and install the required packages. This will also create the input and output folders ('_INPUT' and '_OUTPUT' by default).


## Usage

1. Add the images you want to process to the input folder ('_INPUT' by default).
2. Run the 'run.bat' script. You can choose to run the app with default parameters or interactively to customize the parameters.

- Choose Option 1 to run the app with default parameters specified in 'app.py'.
- Choose Option 2 to run the app interactively, allowing you to customize the following parameters:

  - input_folder: The folder containing the input images (default: '_INPUT')
  - output_folder: The folder to save the processed images (default: '_OUTPUT')
  - offset_x: Horizontal offset of face center (default: 0.0)
  - offset_y: Vertical offset of face center (default: -15.0)
  - face_percent: Size of the face in the resulting photo as a percentage (default: 40.0)
  - resize: Size of the output image (default: 512)
  - threshold: Threshold of face detection (0-1) (default: 0.25)
  - output_format: Output format (jpg, png, etc.) (default: jpg)

3. The processed images will be saved in the output folder ('_OUTPUT' by default).

## License

This project is licensed under the terms of the MIT License.
