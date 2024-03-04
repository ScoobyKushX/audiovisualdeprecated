# mainwindow.py
import pyaudio
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QComboBox, QPushButton, QApplication
import sys
import numpy as np
from vispywidget import VispyWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vispy within PySide6')

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.vispy_widget = VispyWidget()
        layout.addWidget(self.vispy_widget.native)

        self.vispy_widget.show()

class AudioVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.deviceComboBox = QComboBox(self)
        self.populateAudioDevices()
        self.confirmButton = QPushButton('Start Visualization', self)

        self.layout.addWidget(self.deviceComboBox)
        self.layout.addWidget(self.confirmButton)

        self.confirmButton.clicked.connect(self.startVisualization)

        self.setLayout(self.layout)
        self.setWindowTitle('Audio Device Selector')
        self.show()

    def populateAudioDevices(self):
        for i in range(self.p.get_device_count()):
            dev_info = self.p.get_device_info_by_index(i)
            if dev_info['maxInputChannels'] > 0:  # Change to maxOutputChannels for outputs
                self.deviceComboBox.addItem(dev_info['name'], i)

    def startVisualization(self):
        device_index = self.deviceComboBox.currentData()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  input_device_index=device_index,
                                  frames_per_buffer=1024,
                                  stream_callback=self.audioCallback)

        self.stream.start_stream()

    def audioCallback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        # Process the audio_data to update your visualization
        # For example, compute the volume or FFT and update a visual element accordingly
        return (None, pyaudio.paContinue)

    def closeEvent(self, event):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        super().closeEvent(event)

if __name__ == '__main__':
    app2 = QApplication([])
    widget = VispyWidget()
    ex = AudioVisualizer()
    widget.show()
    ex.show()
    sys.exit(app.exec_())
    app2.exec_()