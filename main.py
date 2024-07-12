import sys
import os
import cv2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QTextEdit, QProgressBar, QTabWidget, QMainWindow
)
from PyQt5.QtCore import Qt


class FrameExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label1 = QLabel('Frame Extractor:')
        layout.addWidget(self.label1)

        self.inputBtn1 = QPushButton('Select Input Video')
        self.inputBtn1.clicked.connect(self.selectInputVideo)
        layout.addWidget(self.inputBtn1)

        self.outputBtn1 = QPushButton('Select Output Folder')
        self.outputBtn1.clicked.connect(self.selectOutputFolder1)
        layout.addWidget(self.outputBtn1)

        self.fpsLabel1 = QLabel('Frame Rate:')
        layout.addWidget(self.fpsLabel1)

        self.fpsInput1 = QLineEdit(self)
        layout.addWidget(self.fpsInput1)

        self.extractBtn = QPushButton('Extract Frames')
        self.extractBtn.clicked.connect(self.extractFrames)
        layout.addWidget(self.extractBtn)

        self.progressBar1 = QProgressBar(self)
        layout.addWidget(self.progressBar1)

        self.log1 = QTextEdit(self)
        self.log1.setReadOnly(True)
        layout.addWidget(self.log1)

        self.setLayout(layout)

        self.inputVideo = ''
        self.outputFolder1 = ''
        self.originalFps = 0

    def selectInputVideo(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Input Video", "", "Video Files (*.mp4 *.avi *.mov)",
                                                  options=options)
        if fileName:
            self.inputVideo = fileName
            self.setOriginalFrameRate()

    def setOriginalFrameRate(self):
        cap = cv2.VideoCapture(self.inputVideo)
        if cap.isOpened():
            self.originalFps = int(cap.get(cv2.CAP_PROP_FPS))
            self.fpsInput1.setText(str(self.originalFps))
        cap.release()

    def selectOutputFolder1(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.outputFolder1 = folder

    def log(self, message):
        self.log1.append(message)
        self.log1.verticalScrollBar().setValue(self.log1.verticalScrollBar().maximum())

    def extractFrames(self):
        if not self.inputVideo or not self.outputFolder1 or not self.fpsInput1.text().isdigit():
            QMessageBox.warning(self, "Error", "Please provide valid input video, output folder, and frame rate.")
            return

        frame_rate = int(self.fpsInput1.text())

        cap = cv2.VideoCapture(self.inputVideo)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(original_fps / frame_rate)

        self.progressBar1.setMaximum(total_frames // frame_interval)
        self.progressBar1.setValue(0)
        frame_idx = 0
        saved_frame_idx = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % frame_interval == 0:
                frame_filename = os.path.join(self.outputFolder1, f"frame_{saved_frame_idx:06d}.jpg")
                cv2.imwrite(frame_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                self.log(f"Extracted {frame_filename}")
                saved_frame_idx += 1
                self.progressBar1.setValue(saved_frame_idx)
            frame_idx += 1

        cap.release()

        with open(os.path.join(self.outputFolder1, "FRAME_RATE.txt"), 'w') as f:
            f.write(str(frame_rate))

        QMessageBox.information(self, "Success", "Frames extracted successfully.")


class VideoAssembler(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label2 = QLabel('Video Assembler:')
        layout.addWidget(self.label2)

        self.inputBtn2 = QPushButton('Select Input Folder')
        self.inputBtn2.clicked.connect(self.selectInputFolder2)
        layout.addWidget(self.inputBtn2)

        self.fpsLabel2 = QLabel('Frame Rate:')
        layout.addWidget(self.fpsLabel2)

        self.fpsInput2 = QLineEdit(self)
        layout.addWidget(self.fpsInput2)

        self.outputBtn2 = QPushButton('Select Output Video Destination')
        self.outputBtn2.clicked.connect(self.selectOutputVideo)
        layout.addWidget(self.outputBtn2)

        self.assembleBtn = QPushButton('Assemble Video')
        self.assembleBtn.clicked.connect(self.assembleVideo)
        layout.addWidget(self.assembleBtn)

        self.progressBar2 = QProgressBar(self)
        layout.addWidget(self.progressBar2)

        self.log2 = QTextEdit(self)
        self.log2.setReadOnly(True)
        layout.addWidget(self.log2)

        self.setLayout(layout)

        self.inputFolder2 = ''
        self.outputVideo = ''

    def selectInputFolder2(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.inputFolder2 = folder

    def selectOutputVideo(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Select Output Video Destination", "",
                                                  "Video Files (*.mp4 *.avi *.mov)", options=options)
        if fileName:
            self.outputVideo = fileName

    def log(self, message):
        self.log2.append(message)
        self.log2.verticalScrollBar().setValue(self.log2.verticalScrollBar().maximum())

    def assembleVideo(self):
        if not self.inputFolder2 or not self.fpsInput2.text().isdigit() or not self.outputVideo:
            QMessageBox.warning(self, "Error",
                                "Please provide valid input folder, frame rate, and output video destination.")
            return

        frame_rate = int(self.fpsInput2.text())

        images = [img for img in sorted(os.listdir(self.inputFolder2)) if img.endswith(".jpg")]
        if not images:
            QMessageBox.warning(self, "Error", "No images found in the selected folder.")
            return

        self.progressBar2.setMaximum(len(images))
        self.progressBar2.setValue(0)

        first_image = cv2.imread(os.path.join(self.inputFolder2, images[0]))
        height, width, layers = first_image.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec as needed
        video = cv2.VideoWriter(self.outputVideo, fourcc, frame_rate, (width, height))

        for idx, image in enumerate(images):
            img_path = os.path.join(self.inputFolder2, image)
            frame = cv2.imread(img_path)
            video.write(frame)
            self.log(f"Added {img_path} to video")
            self.progressBar2.setValue(idx + 1)

        video.release()

        QMessageBox.information(self, "Success", "Video assembled successfully.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Video Frame Extractor and Assembler')
        self.setGeometry(100, 100, 600, 400)

        self.tabWidget = QTabWidget()
        self.frameExtractorTab = FrameExtractor()
        self.videoAssemblerTab = VideoAssembler()

        self.tabWidget.addTab(self.frameExtractorTab, 'Frame Extractor')
        self.tabWidget.addTab(self.videoAssemblerTab, 'Video Assembler')

        self.setCentralWidget(self.tabWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
