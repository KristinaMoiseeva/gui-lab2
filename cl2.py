from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class DollarSignal(QObject):
    """Источник пользовательского сигнала изменения значения USD."""

    changed = pyqtSignal(float)

    @pyqtSlot(float)
    def emit_value(self, value):
        self.changed.emit(value)
