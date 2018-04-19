import socket, pickle,random,time

class Sender:
    def __init__(self, host, port):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((hote, port))
        print("Connection on {}".format(port))


    def send(self, pixels):
        data = pickle.dumps(pixels, protocol=2)
        self.socket.send(data)




hote = "10.42.0.27"
port = 15555

s = Sender(hote, port)
i = 0
while True:
    s.send([449])
    i+=1
    if i == 450:
        i = 0
    time.sleep(1/50.)
