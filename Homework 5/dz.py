from PyQt5.QtWidgets import *


class ModelessDialog(QDialog):
    def __init__(self, part, threshold, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Baseline")
        self.setGeometry(800, 275, 300, 200)
        self.part = part
        self.threshold = threshold
        self.threshNew = 0

        label = QLabel("Начало           : {}\nКонец   : {}".format(
            self.part, self.threshold))
        self.label2 = QLabel("Пиши что-нибудь уже".format(self.threshNew))

        self.spinBox = QDoubleSpinBox()


        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok
            | QDialogButtonBox.Cancel
            | QDialogButtonBox.Apply)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.label2)
        layout.addWidget(self.spinBox)
        layout.addWidget(buttonBox)
        self.resize(200, 200)
        self.setLayout(layout)

        #Кнопка выдает результат "Все работает"
        okBtn = buttonBox.button(QDialogButtonBox.Ok)
        okBtn.clicked.connect(self._okBtn)

        #Кнопка Cancel не пропадает
        cancelBtn = buttonBox.button(QDialogButtonBox.Cancel)
        cancelBtn.clicked.connect(self.reject)

        #Кнопка Apply выдает результат "Применяется"
        applyBtn = buttonBox.button(QDialogButtonBox.Apply)
        applyBtn.clicked.connect(self._apply)

    def _apply(self):
        print('Применяется')

    def _okBtn(self):
        print('Все работает')

    def valueChang(self):
        self.label2.setText("Пиши что-нибудь та уже".format(self.spinBox.value()))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel('Hello Dialog', self)
        button = QPushButton('Open Dialog', self)
        button.clicked.connect(self.showDialog)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

    def showDialog(self):
        self.dialog = ModelessDialog('Сегодня', 'Завтра',  self)
        self.dialog.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = Window()
    win.resize(300, 200)
    win.show()
    sys.exit(app.exec_())