# Modules
import json
import os
import sys

# Load File
if not os.path.exists('data.json'):
    print('"data.json" adlı dosya bulunamadı!')
    sys.exit()

with open('data.json', 'r') as file:
    data = json.load(file)

def apply(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Console
while True:
    cmd=input('>>> ')
    if cmd.lower()=='authorize':
        user=f'{input()}'
        data['_Authorized_Users'][user] = data['_Unuthorized_Users'][user]
        del data['_Unuthorized_Users'][user]
        apply(data)
    elif cmd.lower()=='unuthorize':
        user=f'{input()}'
        data['_Unuthorized_Users'][user] = data['_Authorized_Users'][user]
        del data['_Authorized_Users'][user]
        apply(data)
    elif cmd.lower()=='delete':
        user=f'{input()}'

        if user in data['_Unuthorized_Users']:
            del data['_Unuthorized_Users'][user]

        if user in data['_Authorized_Users']:
            del data['_Authorized_Users'][user]

        apply(data)
