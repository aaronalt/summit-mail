from PySide2.QtCore import QThread, QObject, Signal, Qt
from PySide2.QtWidgets import QApplication

gui_thread = None
qt_app = None


class Application(QApplication):

    def __init__(self, qargs=None):
        QApplication.__init__(self, qargs)
        self.setStyle("Fusion")
        self.setApplicationName("SummitMail(er)")
        global gui_thread, qt_app
        gui_thread = QThread.currentThread()
        qt_app = self
        print("Application initialized from __init__.py...")


class Dispatcher(QObject):
    """
    Convenience class to use Qt signals with arbitrary python callables.
    By default, ensures that a function call always happens in the
    thread this Dispatcher was created in.
    Note that if you create the Dispatcher in a thread without an event loop of
    its own, the function call will happen in the GUI thread (I think).
    """
    dispatch_signal = Signal(object, object)

    def __init__(self, function, queued=True, parent=None):
        QObject.__init__(self, parent)
        self.function = function
        connection = Qt.QueuedConnection
        if not queued:
            connection = Qt.AutoConnection if queued is None else Qt.DirectConnection
        self.dispatch_signal.connect(self.dispatch, type=connection)

    def __call__(self, *args, **kwargs):
        self.dispatch_signal.emit(args, kwargs)

    def dispatch(self, args, kwargs):
        self.function(*args, **kwargs)