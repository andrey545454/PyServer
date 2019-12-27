import socket
import threading
import select
import time
import configparser

from random import choice

class PyServer():
    """
    Our server
    """

    def __init__(self, addr):
        # Адрес сервера
        self.ip = addr[0]
        self.port = addr[1]

        # Хранение всех подключений
        self.conns = dict()


    def __enter__(self):
        """
        Создание и настройка сервера

        bind - Привязка сокета к адресу
        setblocking - Установка блокирующего/неблокирующего режима сокета
        listen - Даёт возможность серверу принимать подключения.

        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind((self.ip, self.port))
        self.sock.setblocking(False)
        self.sock.listen()

    def run(self):

        # Запуск потока запланированных задач (выполнение задач каждые t секунд)
        self.schedule_task(10)

        while True:
            try:
                # Пробуем получить новое сокет подключение
                conn, addr = self.sock.accept()
                # Если есть новое подключение, то обрабатываем его
                if conn:
                    # Добавляем новое подключение в словарь
                    self.conns.update({addr: conn})
                    # Выполняем это подключение в новом потоке
                    t = threading.Thread(target=self.client_thread, args=(conn, addr))
                    t.start()
            except:
                pass

    def client_thread(self, connection, address):
        """
        Потоки для клиентов, подключённых к серверу
        """
        print("Новое подключение", address)

        is_active = True
        while is_active:
            # Проверяем сокет на доступность к чтению/записи и на ошибки
            rdy_read, rdy_write, errors = select.select([connection],[connection], [], 5)

            if rdy_read:
                try:
                    data = self.get_data(connection)
                except socket.error:
                    is_active = False
            if rdy_write:
                try:
                    self.create_response(connection)
                except socket.error:
                    is_active = False

        # Делаем уборку
        del self.conns[address]
        print("Отключение", address)
        connection.close()

    def get_data(self, conn, bytes=1024):
        """
        Получение даты из сокета
        """
        return conn.recv(bytes)


    def create_response(self, conn, msg="", enc='UTF-8'):
        """
        Отправка данных в сокет
        """
        conn.sendall(msg.encode(enc))


    def schedule_task(self, t):
        """
        Обработка запланированных задач
        """
        threading.Timer(t, self.schedule_task, args=(t,)).start()

        # Выбираем рандомную фразу из файла
        with open("messages.txt", encoding="UTF-8") as file:
            msg = choice(file.readlines())
        # Перебор всех подключений и отправка сообщения
        for addr in self.conns:
            self.create_response(self.conns[addr], msg)


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрытие сервера
        """
        self.sock.close()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    HOST, PORT = config["Server"]["server_ip"], int(config["Server"]["server_port"])

    # Create the server, binding to localhost on port 50007
    server = PyServer((HOST, PORT))
    with server:
        server.run()