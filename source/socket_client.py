import socket


class SocketClient:
    '''Socket Client'''

    def __init__(self, parent, host, port):
        self.parent = parent
        self.host = host
        self.port = port
        self.sock = None

    def try_send_file_open(self, file_path):
        received_data = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.host, self.port))
                sock.sendall(str.encode(file_path))
                received_data = sock.recv(1024)
            except:
                received_data = None

        print('Received', repr(received_data))
        return received_data is not None
