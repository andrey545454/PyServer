import socket
import threading
import socketserver
import time
import queue


class PyServer():
    """
    Our server
    """

    def __init__(self):
        pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 50007

    # Create the server, binding to localhost on port 50007
    server = PyServer((HOST, PORT))
    with server:
        ip, port = server.server_address