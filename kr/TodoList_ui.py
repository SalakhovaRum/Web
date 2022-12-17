import socket
import sqlite3
import threading
import TodoList

from PyQt5.QtWidgets import QMainWindow, QApplication

#Создаем базу данных и подключаемся к ней
conn = sqlite3.connect('mylist.db')
c = conn.cursor()

#Создаем таблицу
c.execute("""CREATE TABLE if not exists todo_list(list_item text)""")

#Зафиксируем изменения
conn.commit()

#Закроем нашу связь
conn.close()


# пишем своё MainWindow, основанное на Ui_MainWindow (которое мы ранее сгенерировали)
class ToDoList(QMainWindow, TodoList.Ui_MainWindow):
    def __init__(self):
        #устанавливаем элементы интерфейса
        super(ToDoList, self).__init__()
        self.setupUi(self)

        # создаем сокет и подключаемся к сокет-серверу
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 5040))
        self.ok.clicked.connect(self.nickname_was_chosen)
        self.send.clicked.connect(self.add)

    # функция, которая выполняется при нажатии кнопки "ОК"
    def nickname_was_chosen(self):
        # открываем возможность ввода заметок
        self.msg_line.setEnabled(True)
        self.send.setEnabled(True)
        # блокируем возможность ввода другого никнейма
        self.nickname.setEnabled(False)
        self.ok.setEnabled(False)

        # отправляем сокет-серверу введённый никнейм
        self.client.send(self.nickname.text().encode('ascii'))

        # стартуем поток, который постоянно будет пытаться получить заметки
        add_thread = threading.Thread(target=self.add)
        add_thread.start()

    # метод для получения заметок от других клиентов
    def receive(self):
        while True:
            try:
                # пытаемся получить заметку
                note = self.client.recv(1024).decode('ascii')
                # добавляем заметки в список
                if not note.startswith("NICK") and not note.startswith(self.nickname.text()):
                    self.messages.append(note)
            except:
                # в  случае ошибок выводится Error! Reload app
                self.msg_line.setText("Error! Reload app")
                self.msg_line.setEnabled(False)
                self.send.setEnabled(False)
                # закрываем клиента
                self.client.close()
                break


    # метод, который редактирует заметки
    def edit(self):
        #Сопоставляем заметки
        note = '{}: {}'.format(self.nickname.text(), self.msg_line.text())
        # добавляем его в общий список заметок
        self.note.add(note)
        #редактируем заметку
        self.client.send(note.encode('ascii'))


    # метод, который удаляет  заметки
    def delete(self):
        # Захватите выбранную строку или текущую строку
        clicked = self.mylist_listWidget.currentRow()
        #Удалите выбранную строку
        self.mylist_listWidget.takeItem(clicked)

    # метод, который сохраняет заметки после редактирования/удаления/добавления
    def save(self):
        #Поключаемся к базе данных
        connect = sqlite3.connect('mylist.db')

        #Зафиксируйте изменения
        connect.commit()

        #Закройте связь
        connect.close()


if __name__ == "__main__":
    app = QApplication([])
    window = ToDoList()
    window.show()
    app.exec()
