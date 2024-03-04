# mainwindow.py

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
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
