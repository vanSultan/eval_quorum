from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class EvalPlot(FigureCanvas):
    def __init__(self, model=None, parent=None):
        figure = Figure()
        self.axes = figure.add_subplot(111)

        self._model = model
        if self._model:
            data = self._model.data
            title = self._model.title
            labels = self._model.labels
        else:
            data = []
            title = 'Пока ничего'
            labels = None

        self.axes.cla()  # Еще 12 часов на эту строчку...
        self.axes.pie(data, labels=labels)
        self.axes.set_title(title)

        FigureCanvas.__init__(self, figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.draw()  # Потратил 2 часа чтобы понять, что нужна эта строчка P.s. в офф примере mpl ее нет -_-

    def model_is_changed(self):
        self.axes.cla()
        # TODO обновить данные
        self.draw()

    @property
    def model(self):
        return self.model

    @model.setter
    def model(self, new_model):
        self._model = new_model
        self.model_is_changed()
