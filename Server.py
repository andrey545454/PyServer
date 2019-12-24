import socketserver


class PyServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)


class TCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    """
    def handle(self):
        # Send data
        self.request.sendall("Hello, world".encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 50007

    # Create the server, binding to localhost on port 50007
    with PyServer((HOST, PORT), TCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()