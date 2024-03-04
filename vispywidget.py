import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from vispy import gloo, app

import shaders
from shaders import vertex_shader, fragment_shader


class VispyWidget(app.Canvas):
    def __init__(self, parent=None):
        app.Canvas.__init__(self, parent=parent, keys='interactive')
        self.program = gloo.Program(vertex_shader, fragment_shader)
        self.init_bars()
        self.show()

    def init_bars(self):
        # Initialize bars
        bar_width = self.size[0] / 10
        self.bars = np.zeros((10, 2, 3), dtype=np.float32)
        for i in range(10):
            self.bars[i, :, 0] = i * bar_width, (i + 1) * bar_width
            self.bars[i, :, 1] = 0, 0.5  # Initial height
            self.bars[i, :, 2] = 0, 0  # z-axis
            self.program['a_position'] = self.bars.reshape(-1, 3)  # Flatten array

    def on_draw(self, event):
        gloo.clear('red')
        self.program.draw('line_strip')

    def update_bars(self, heights):
        # Update bars based on audio data (simulated here)
        for i, height in enumerate(heights):
            self.bars[i, :, 1] = 0, height
        self.program['a_position'] = self.bars.flatten()
        self.update()

if __name__ == '__main__':
    app = QApplication([])
    widget = VispyWidget()
    widget.show()
    app.exec_()