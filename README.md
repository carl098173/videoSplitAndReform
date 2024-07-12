# Video Frame Extractor and Assembler

This project provides a GUI-based application for extracting frames from a video and assembling frames into a video. The application is built using Python and PyQt5, with OpenCV for video processing.

## Features

- **Frame Extractor**: 
  - Select an input video file.
  - Specify an output folder to save the extracted frames.
  - Set the frame rate for extraction (defaulted to the original frame rate of the input video).
  - View a progress bar and logs during the frame extraction process.

- **Video Assembler**: 
  - Select an input folder containing frame images.
  - Specify an output video file destination.
  - Set the frame rate for the video assembly.
  - View a progress bar and logs during the video assembly process.

## Requirements

- Python 3.x
- PyQt5
- OpenCV

## Installation

1. Install Python 3.x if not already installed. You can download it from [python.org](https://www.python.org/).
2. Install the required Python packages using pip:

    ```bash
    pip install pyqt5 opencv-python
    ```

## Usage

1. **Run the Application**:

    ```bash
    python main.py
    ```

2. **Frame Extraction**:
   - Go to the "Frame Extractor" tab.
   - Click on "Select Input Video" to choose your video file.
   - Click on "Select Output Folder" to specify where the extracted frames should be saved.
   - Set the desired frame rate (defaults to the original frame rate of the input video).
   - Click on "Extract Frames" to start the extraction process.
   - The progress bar will update, and logs will be displayed in the text area.

3. **Video Assembly**:
   - Go to the "Video Assembler" tab.
   - Click on "Select Input Folder" to choose the folder containing frame images.
   - Set the desired frame rate for the output video.
   - Click on "Select Output Video Destination" to specify where the assembled video should be saved.
   - Click on "Assemble Video" to start the assembly process.
   - The progress bar will update, and logs will be displayed in the text area.

## Code Overview

The application consists of three main classes:

1. **FrameExtractor**: Handles frame extraction from a video.
2. **VideoAssembler**: Handles video assembly from frame images.
3. **MainWindow**: Manages the main window and tabs of the application.

### FrameExtractor

This class provides a user interface for selecting an input video, specifying an output folder, setting a frame rate, and extracting frames from the video.

### VideoAssembler

This class provides a user interface for selecting an input folder containing frame images, specifying an output video destination, setting a frame rate, and assembling the frames into a video.

### MainWindow

This class initializes the main window with two tabs: "Frame Extractor" and "Video Assembler". It combines the functionality of the FrameExtractor and VideoAssembler classes.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Author

This project was created by [Your Name]. Feel free to reach out if you have any questions or suggestions!
