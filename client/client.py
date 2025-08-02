# Modules
import socket
import os
import random

# Client
IP='127.0.0.1'
PORT=12345
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))


# Send Data
if not os.path.exists('key.key'):
    with open('key.key', 'wb') as file:
        file.write(str(random.randint(11111,99999)).encode())

with open('key.key', 'rb') as file:
    randomKey=file.read()

client.sendall(randomKey)

# Close Connection
client.close()
