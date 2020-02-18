from PyQt5 import QtWidgets
from matplotlib import animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from model.eval_model import EvalModel


class EvalPlot(FigureCanvas):
    def __init__(self, model: EvalModel = None, parent=None):
        self.animation = None
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        self._model = model
        if self._model:
            data = self._model.data
            title = self._model.title
            labels = self._model.labels
            self.update_step(model.get_total())
        else:
            data = []
            title = 'Пока ничего'
            labels = []

        self.axes.cla()  # Еще 12 часов на эту строчку...
        self.pie = self.axes.pie(data, labels=labels)
        self.axes.set_title(title)

        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.draw()  # Потратил 2 часа чтобы понять, что нужна эта строчка P.s. в офф примере mpl ее нет -_-

    def update_figure(self, data: list):
        self.axes.clear()
        self.axes.set_title(self._model.title)
        self.pie = self.axes.pie(data, autopct=lambda pct: '{:.1f}%'.format(pct))
        labels = list(map(lambda x, y: f'{x} - {y}', self._model.labels, data))
        self.axes.legend(self.pie[0], labels, title='Категории',
                         loc='lower right', bbox_to_anchor=(1.17, -0.15))
        self.draw()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, new_model: EvalModel):
        self._model = new_model
        if self._model.get_total() > 0:
            self.animation = animation.FuncAnimation(self.figure, self.update_figure, self.model.data, repeat=False)
            self.animation._start()  # Так делать нельзя, но выбора не было
