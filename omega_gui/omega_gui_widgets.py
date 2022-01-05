"""

"""

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        from matplotlib.figure import Figure

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


from PySide2.QtWidgets import QWidget


class myWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        print('custom widget init!!?')


import PySide2
from PySide2.QtWidgets import QMainWindow


class omegaQMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        pass

    def closeEvent(self, event:PySide2.QtGui.QCloseEvent) -> None:
        # could do any cleanup or saving here, if we wanted to
        pass

    def resizeEvent(self, event:PySide2.QtGui.QResizeEvent) -> None:
        try:
            # print('resize %s, %s !!' % (self.plot_widget.size(), self.plot_scroll.size()))

            # don't need to do this:
            # self.result_plots[0].resize(self.plot_scroll.width() - 40,
            #                             self.plot_scroll.height() * 0.9)
            # self.result_plots[1].resize(self.plot_scroll.width() - 40,
            #                             self.plot_scroll.height() * 0.9)

            # resizing the widget resizes the plots automatically:
            # self.plot_widget.resize(self.plot_scroll.width() - 20,
            #                         self.plot_scroll.height() * 0.96 * len(self.result_plots))
            self.plot_widget.resize(self.plot_scroll.width() - 20,
                                    self.plot_scroll.height() * len(self.result_plots) - 34)
        except:
            pass
