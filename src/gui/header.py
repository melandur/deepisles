from PyQt5 import  QtWidgets


class Header(QtWidgets.QMainWindow):
    """Defines Software header with title name and icon"""

    def __init__(self, mw, user_specs):
        super().__init__()
        self.mw = mw
        width, height = user_specs.user_specs['Primary_Screen_Available_Size']
        self.mw.setGeometry(int(width / 6), int(height / 8), int(width / 1.7), int(height / 1.3))  # define main window size
        self.mw.setWindowTitle('DeepISLES')


