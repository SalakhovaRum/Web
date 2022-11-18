from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

#Создаем класс Window
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Крестики-нолики")
        self.setGeometry(200, 200,
                         300, 500)
        self.UiComponents()
        self.show()

    def UiComponents(self):
        self.turn = 0
        self.times = 0
        self.push_list = []

        # creating 2d list
        for i in range(3):
            temp = []
            for i in range(3):
                temp.append((QPushButton(self)))
            # adding 3 push button in single row
            self.push_list.append(temp)

        # Координаты x и y
        x = 90
        y = 90

        #Перемещение по списку кнопок
        for i in range(3):
            for j in range(3):
                #Настройка геометрии для кнопок
                self.push_list[i][j].setGeometry(x * i + 20,
                                                 y * j + 20,
                                                 80, 80)
                #Настройка шрифта для кнопок
                self.push_list[i][j].setFont(QFont(QFont('Times', 17)))
                #Добавления действия
                self.push_list[i][j].clicked.connect(self.action_called)

        #Создание ярлыка для определения счета
        self.label = QLabel(self)
        self.label.setGeometry(20, 300, 260, 60)
        #Настройка стилей для таблицы
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 3px solid black;"
                                 "background : white;"
                                 "}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Times', 15))

        #Создание кнопки для перезапуска счета
        reset_game = QPushButton("Restart", self)
        reset_game.setGeometry(50, 380, 200, 50)

        #Добавления действия к кнопке сброса
        reset_game.clicked.connect(self.reset_game_action)

    #Метод вызываемой кнопкой сброса
    def reset_game_action(self):
        self.turn = 0
        self.times = 0
        self.label.setText("")

        #Нужен чтобы рестар делать и все обновлялось
        for buttons in self.push_list:
            for button in buttons:
                button.setEnabled(True) #Включение всех кнопок
                button.setText("") #Удаление текста со всех кнопок

    def action_called(self):
        self.times += 1
        button = self.sender()
        button.setEnabled(False)

        if self.turn == 0:
            button.setText("X")
            self.turn = 1
        else:
            button.setText("O")
            self.turn = 0

        #Вызывается метод выбора победителя
        win = self.who_wins()
        text = ""

        #Если победитель опреелен
        if win == True:
            if self.turn == 0:
                text = "O Выиграл"
            else:
                text = "X Выиграл"

            #Отключение всех кнопок
            for buttons in self.push_list:
                for push in buttons:
                    push.setEnabled(False)

        #Если победитель не определен и 9 шансов исчерпаны
        elif self.times == 9:
            text = "Ничья"
        self.label.setText(text)

    #Способ проверки победителя
    def who_wins(self):
        #Проверка  пересеклась ли какая-либо строка
        for i in range(3):
            if self.push_list[0][i].text() == self.push_list[1][i].text() \
                    and self.push_list[0][i].text() == self.push_list[2][i].text() \
                    and self.push_list[0][i].text() != "":
                return True

        #Проверка пересеклись ли какие-либо столбцы
        for i in range(3):
            if self.push_list[i][0].text() == self.push_list[i][1].text() \
                    and self.push_list[i][0].text() == self.push_list[i][2].text() \
                    and self.push_list[i][0].text() != "":
                return True

        #Проверка на пересечение 1 диагонали
        if self.push_list[0][0].text() == self.push_list[1][1].text() \
                and self.push_list[0][0].text() == self.push_list[2][2].text() \
                and self.push_list[0][0].text() != "":
            return True

        #Проверка на пересечение 2 диагонали
        if self.push_list[0][2].text() == self.push_list[1][1].text() \
                and self.push_list[1][1].text() == self.push_list[2][0].text() \
                and self.push_list[0][2].text() != "":
            return True
        #Если ничего не пересечено
        return False


if __name__ == '__main__':
    import sys

App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())