import sys

from PyQt5.QtCore import QObject, QSignalBlocker, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from cl1 import RubleSignal
from cl2 import DollarSignal


USD_TO_RUB = 100.0
EUR_TO_RUB = 110.0


class EuroSignal(QObject):
    """Источник пользовательского сигнала изменения значения EUR."""

    changed = pyqtSignal(float)

    @pyqtSlot(float)
    def emit_value(self, value):
        self.changed.emit(value)


class CurrencyConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Лабораторная работа №2 — сигналы и слоты")
        self.resize(460, 300)

        self.ruble_signal = RubleSignal()
        self.dollar_signal = DollarSignal()
        self.euro_signal = EuroSignal()

        self.usd = self.create_spinbox(" USD", decimals=4)
        self.rub = self.create_spinbox(" RUB", decimals=2)
        self.eur = self.create_spinbox(" EUR", decimals=4)

        self.build_ui()
        self.connect_signals()

        # Начальное значение: 1 USD.
        self.usd.setValue(1.0)

    @staticmethod
    def create_spinbox(suffix, decimals):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(0.0, 1_000_000_000.0)
        spinbox.setDecimals(decimals)
        spinbox.setSingleStep(1.0)
        spinbox.setSuffix(suffix)
        return spinbox

    def build_ui(self):
        title = QLabel("Конвертер валют")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        rates = QLabel(
            f"Демонстрационные курсы:\n"
            f"1 USD = {USD_TO_RUB:.2f} RUB\n"
            f"1 EUR = {EUR_TO_RUB:.2f} RUB"
        )

        form = QFormLayout()
        form.addRow("Доллар:", self.usd)
        form.addRow("Рубль:", self.rub)
        form.addRow("Евро:", self.eur)

        group = QGroupBox("Значения валют")
        group.setLayout(form)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(rates)
        layout.addWidget(group)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def connect_signals(self):
        # Стандартный сигнал valueChanged каждого поля передаём
        # отдельному объекту, который испускает пользовательский сигнал changed.
        self.usd.valueChanged.connect(self.dollar_signal.emit_value)
        self.rub.valueChanged.connect(self.ruble_signal.emit_value)
        self.eur.valueChanged.connect(self.euro_signal.emit_value)

        # Пользовательские сигналы связываем со слотами пересчёта.
        self.dollar_signal.changed.connect(self.on_usd_changed)
        self.ruble_signal.changed.connect(self.on_rub_changed)
        self.euro_signal.changed.connect(self.on_eur_changed)

    @pyqtSlot(float)
    def on_usd_changed(self, usd_value):
        rub_value = usd_value * USD_TO_RUB
        eur_value = rub_value / EUR_TO_RUB
        self.set_values(rub=rub_value, eur=eur_value)

    @pyqtSlot(float)
    def on_rub_changed(self, rub_value):
        usd_value = rub_value / USD_TO_RUB
        eur_value = rub_value / EUR_TO_RUB
        self.set_values(usd=usd_value, eur=eur_value)

    @pyqtSlot(float)
    def on_eur_changed(self, eur_value):
        rub_value = eur_value * EUR_TO_RUB
        usd_value = rub_value / USD_TO_RUB
        self.set_values(usd=usd_value, rub=rub_value)

    def set_values(self, usd=None, rub=None, eur=None):
        """
        Обновляет поля программно.

        QSignalBlocker нужен, чтобы программное setValue() не запускало
        повторную цепочку сигналов и не создавало зацикливание.
        """
        blockers = []

        try:
            if usd is not None:
                blockers.append(QSignalBlocker(self.usd))
                self.usd.setValue(usd)

            if rub is not None:
                blockers.append(QSignalBlocker(self.rub))
                self.rub.setValue(rub)

            if eur is not None:
                blockers.append(QSignalBlocker(self.eur))
                self.eur.setValue(eur)
        finally:
            blockers.clear()


def main():
    app = QApplication(sys.argv)

    window = CurrencyConverter()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
