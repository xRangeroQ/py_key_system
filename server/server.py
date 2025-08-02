# Modules
import sys
import socket
import os
import subprocess
from cryptography.fernet import Fernet
import json
import threading
from colorama import Style, Fore

# Styles
reset=Style.RESET_ALL
green=Fore.LIGHTGREEN_EX
red=Fore.LIGHTRED_EX
yellow=Fore.LIGHTYELLOW_EX

# Fernet Key
if not os.path.exists('server_key.key'):
    with open('server_key.key', 'wb') as file:
        file.write(Fernet.generate_key())
        print(f'[{green}+{reset}] "server_key.key" dosyası bulunamadığı için yeni bir tane oluşturuldu ve bütün veriler silindi!')
        if os.path.exists('data.json'):
            os.remove('data.json')

with open('server_key.key', 'rb') as file:
    key = Fernet(file.read())

# Data File
if not os.path.exists('data.json'):
        with open('data.json', 'w') as f:
            f.write('{\n    "_Unuthorized_Users": {},\n    "_Authorized_Users": {},\n    "_Queue": 0\n}')
            print(f'[{green}+{reset}] "data.json" dosyası bulunamadığı için yeni bir tane oluşturuldu!')

# Start Server
def start():
    # Server
    IP='0.0.0.0'
    PORT=12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()
    print(f'[{green}+{reset}] Sunucu {(yellow)+(str(PORT))+(reset)} portunda dinleniyor.')
    subprocess.Popen(['start', 'cmd', '/k', sys.executable, '-m', 'console.py'], shell=True)

    threads=threading.Thread(target=getcon, args=(server,))
    threads.start()

# Data
def proccess(conn, addr):
    # New Data
    recvData = conn.recv(1024)

    with open('data.json', 'r') as f:
        data = json.load(f)

    clientip=[]
    queue=data['_Queue']

    for keys in data['_Unuthorized_Users'].keys():
        clientip.append(keys.split(':')[1])

    if addr[0] not in clientip:
        if not recvData:
            print(f"[{red}~{reset}] Kullanıcı'dan veri gelmedi!")
            data['_Unuthorized_Users'][f'{queue}:{addr[0]}'] = None
            data['_Queue'] = data['_Queue'] + 1
        else:
            data['_Unuthorized_Users'][f'{queue}:{addr[0]}'] = key.encrypt(recvData).decode()
            data['_Queue'] = data['_Queue'] + 1

        with open('data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print(f'[{red}~{reset}] Kullanıcı zaten listede bulunuyor!')


# Connections
def getcon(server,):
    while True:
        # Accept Connections
        conn, addr = server.accept()
        print(f'[{green}+{reset}] Yeni bağlantı! {addr}')

        thread=threading.Thread(target=proccess, args=(conn, addr))
        thread.start()
            

# Main
if __name__ == '__main__':
    start()
