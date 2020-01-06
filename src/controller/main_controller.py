from main_view import MainView


class MainController:
    def __init__(self):
        self.c_view = MainView(self)

        self.c_view.show()
