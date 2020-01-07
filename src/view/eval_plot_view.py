from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class EvalPlot(FigureCanvas):
    def __init__(self, model=None, parent=None):
        figure = Figure()
        self.axes = figure.add_subplot(111)

        self._model = model
        data = self._model.data if self._model else list()
        self.axes.pie(data)

        super().__init__(figure)
        self.setParent(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.updateGeometry()

        self.draw()  # Потратил 2 часа чтобы понять, что нужна эта строчка P.s. в офф примере mpl ее нет -_-

    @property
    def model(self):
        return self.model

    @model.setter
    def model(self, new_model):
        self._model = new_model
