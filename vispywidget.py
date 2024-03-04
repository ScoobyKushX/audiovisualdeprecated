# vispywidget.py

from vispy import app, gloo
import numpy as np
from shaders import vertex_shader, fragment_shader
from PySide6 import QtOpenGLWidgets, QtWidgets, QtCore, QtGui

class VispyWidget(app.Canvas):
    def __init__(self):
        self.opengl = QtOpenGLWidgets.QOpenGLWidget()
        app.Canvas.__init__(self, keys='interactive', size=(800, 500))
        self.program = gloo.Program(vertex_shader, fragment_shader)
        self.init_bars()
        gloo.set_viewport(0, 0, *self.physical_size)

    def init_bars(self):
        # Initialize the coordinates for 10 bars, each represented by 2 points (top and bottom)
        self.bars = np.zeros((20, 2), dtype=np.float32)  # 10 bars x 2 points per bar
        for i in range(10):
            x = i * 0.1  # Adjust the x spacing
            self.bars[i * 2] = [x, 0]  # Bottom point
            self.bars[i * 2 + 1] = [x, 1]  # Top point (initial height set to 0.5)
        self.program['a_position'] = self.position
        self.program['u_color'] = (1, 1, 1, 1)  # Set color to white

    def on_draw(self, event):
        gloo.clear('black')
        # Draw the bars as lines
        for i in range(0, len(self.bars), 2):
            self.program['a_position'] = self.bars[i:i+2]
            self.program.draw('lines')

    def update_bars(self, heights):
        # Update the heights of the bars
        for i, height in enumerate(heights):
            self.bars[i * 2 + 1][1] = height  # Update the y-coordinate of the top point
        self.program['a_position'] = self.bars
        self.update()

if __name__ == '__main__':
    c = VispyWidget()
    c.show()
    app.run()