import socket
import pickle

socket.listen(5)
client, address = socket.accept()
print("{} connected".format( address ))
# Create NeoPixel object with appropriate configuration.

while True:
        try:
            response = pickle.loads(client.recv(255))
        except:
            print("smthg wrong happen")

        if response != "":
                    print(response)




print("Close")
client.close()
