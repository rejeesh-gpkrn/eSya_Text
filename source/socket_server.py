import socket
import threading


class SocketServer(threading.Thread):
    '''Socket Listener'''

    def __init__(self, parent, host, port):
        threading.Thread.__init__(self)
        self.parent = parent
        self.threadID = port
        self.name = host
        self.host = host
        self.port = port
        self.sock = None
        self.create_socket()

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        try:
            self.sock.listen(1)
            client, address = self.sock.accept()
        except:
            return False

        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    print('Received', data.decode())
                    self.parent.read(data.decode())
                    response = b'received'
                    client.send(response)
                else:
                    print('Client disconnected')
                    client.close()
                    return True
            except:
                print('Exception on socket')
                client.close()
                return False

    def run(self):
        print("Listening " + self.name)
        while self.sock is not None:
            self.listen()

    def destroy_socket(self):
        #self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.sock.detach()
        #self.sock.shutdown(socket.SHUT_RDWR)
        self.sock = None
