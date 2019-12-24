import socket
import threading
import socketserver
import time
import queue


class PyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    Our server
    """

    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)

        self.lasttime = time.time()

    def service_actions(self):
        # Если прошло 10 секунд, то отправляет сообщение
        if time.time()-self.lasttime >= 10.0:
            self.lasttime = time.time()
            #TODO: Алгоритм отправки сообщений каждому пользователю


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    """
    def setup(self):
        # Setup connection
        print("Подключение пользователя к серверу")

    def handle(self):
        # Handle data
        self.request.send("Привет, пользователь :)".encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 50007

    # Create the server, binding to localhost on port 50007
    with PyServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        ip, port = server.server_address
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        print("Server loop running in thread:", server_thread.name)
        server_thread.run()