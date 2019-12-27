import socket
import threading
import socketserver
import selectors
import time
import queue


class PyServer():
    """
    Our server
    """

    def __init__(self, addr):
        # Адрес сервера
        self.ip = addr[0]
        self.port = addr[1]

        # Потоки
        self._threads = []


    def __enter__(self):
        """
        Создание и настройка сервера

        bind - Привязка сокета к адресу
        setblocking - Установка блокирующего/неблокирующего режима сокета
        listen - Макс. количество подключений

        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind((self.ip, self.port))
        self.sock.setblocking(False)
        self.sock.listen(10)

    def run(self):

        while True:
            try:
                # Пробуем получить новое сокет подключение
                conn, addr = self.sock.accept()
                # Если есть новое подключение, то обрабатываем его
                if conn:
                    t = threading.Thread(target=self.client_thread, args=(conn, addr))
                    self._threads.append(t)
                    t.start()
            except:
                pass

    def client_thread(self, connection, address):
        """
        Потоки для клиентов, подключённых к серверу
        """
        is_active = True
        while is_active:
            pass

        connection.close()


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