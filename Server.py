import socket
import threading
import select
import time


class PyServer():
    """
    Our server
    """

    def __init__(self, addr):
        # Адрес сервера
        self.ip = addr[0]
        self.port = addr[1]

        # Таймер для отправки сообщений каждые 10 секунд
        self.timer = time.time()


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

        while True:
            try:
                # Пробуем получить новое сокет подключение
                conn, addr = self.sock.accept()
                # Если есть новое подключение, то обрабатываем его
                if conn:
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
                    self.create_msg(connection)
                except socket.error:
                    is_active = False


        print("Отключение", address)
        connection.close()

    def get_data(self, conn, bytes=1024):
        """
        Получение даты из сокета
        """
        return conn.recv(bytes)


    def create_msg(self, conn, enc='UTF-8'):
        """
        Отправка данных в сокет
        """
        if time.time()-self.timer >= 10:
            msg = "Hello from server"
            self.timer = time.time()

            conn.sendall(bytes(msg, encoding=enc))

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрытие сервера
        """
        self.sock.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 50007

    # Create the server, binding to localhost on port 50007
    server = PyServer((HOST, PORT))
    with server:
        server.run()