import socket
import select

HOST = 'localhost'    # The remote host
PORT = 50007          # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.setblocking(False)
    while True:
        rdy_read, rdy_write, errors = select.select([s], [s], [], 5)
        if rdy_read:
            print(s.recv(1024))