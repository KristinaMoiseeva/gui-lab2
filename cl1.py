from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class RubleSignal(QObject):
    """Источник пользовательского сигнала изменения значения RUB."""

    changed = pyqtSignal(float)

    @pyqtSlot(float)
    def emit_value(self, value):
        self.changed.emit(value)
