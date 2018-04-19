import socket, pickle,random,time

class Client:
    def __init__(self, host, port):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        print("Connection on {}".format(port))


    def send(self, pixels):
        data = pickle.dumps(pixels, protocol=2)
        self.socket.send(data)
