import socket
from time import sleep

HOST = 'localhost'    # The remote host
PORT = 50007          # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.setblocking(False)
    while True:
        msg = b"hi"
        s.sendall(msg)