# vispywidget.py

from vispy import app, gloo
import numpy as np
from shaders import vertex_shader, fragment_shader
from PySide6 import QtOpenGLWidgets, QtWidgets, QtCore, QtGui



class VispyWidget(app.Canvas):
    def __init__(self):
        self.opengl = QtOpenGLWidgets.QOpenGLWidget()
        opengl = self.opengl
        opengl.setFormat(QtGui.QSurfaceFormat())
        opengl.addWidget(QtGui.QOpenGLContext())
        opengl.setUpdateBehavior(self.update_bars())
        app.Canvas.__init__(self, keys='interactive', size=(800, 500))
        self.program = gloo.Program(vertex_shader, fragment_shader)

        self.init_bars()
        gloo.set_viewport(0, 0, *self.physical_size)

    def init_bars(self):
        # Ici, définissez les coordonnées de vos rectangles/barres
        self.bars = np.zeros((40, 2), dtype=np.float32)  # 10 barres x 4 points par barre
        # La logique pour initialiser les barres doit être ajoutée ici
        self.program['a_position'] = self.bars
        self.program['u_color'] = (1, 1, 1, 1)  # Blanc

    def on_draw(self, event):
        gloo.clear('black')
        # Dessinez vos barres ici
        self.program.draw('line_loop')  # Corrigé pour éviter l'avertissement

    def update_bars(self, heights):
        self.bars[:, 1] = heights
        self.update()
        # Mettez à jour les hauteurs des barres ici et appelez self.update() à la fin
        pass


if __name__ == '__main__':
    c = VispyWidget()
    c.show()
    app.run()
