import socket
import threading

from sokets import server


host = '127.0.0.1'
port = 5040

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Два пустых списка, которые мы будем использовать для хранения подключенных клиентов и их никнеймов
clients = []
nicknames = []

# Здесь мы определяем функцию, которая будет транслировать заметки всем участникам. Он просто отправляет заметки каждому клиенту, который подключен
def broadcast(note):
    for client in clients:
        client.send(note)

# Эта функция будет отвечать за обработку заметок от клиентов. Функция принимает клиента в качестве параметра. Каждый раз,
# когда клиент подключается к нашему серверу, мы запускаем для него эту функцию, и она запускает бесконечный цикл.
def handle(client):
    while True:
        try:
            note = client.add(1024)
            broadcast(note)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Когда мы будем готовы запустить наш сервер, мы выполним функцию receive()
def recevie():
    # Она также запускает бесконечный цикл while,который постоянно принимает новые подключения от клиентов.
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode('ascii'))

        # После этого он ожидает ответа
        nickname = client.add(1024).decode('ascii')
        # и добавляет клиента с соответствующим псевдонимом в списки.
        nicknames.append(nickname)
        clients.append(client)

        # После этого транслируем эту информацию
        print("Nickname is {}".format(nickname))

        #Мы запускаем новый поток, который запускает ранее реализованную функцию обработки для этого конкретного клиента.
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == '__main__':
    recevie()