from socket import *
import json
import time
import argparse
presence = {
"action": "presence",
"time": '',
"type": "status",
"user": {
"account_name": "Makuhin",
"status": "Hello, I am here!"}
}

parser = argparse.ArgumentParser(description='ip, port')
parser.add_argument("-p", dest='port', default=7777, type=int)
parser.add_argument("-a", dest='ip', default='localhost')
args = parser.parse_args()
print(args)
port,ip = args.port, args.ip

def main():
    presence['time'] = time.time()
    s = socket(AF_INET, SOCK_STREAM) # Создать сокет TCP
    s.connect((ip, port)) # Соединиться с сервером
    s.send(json.dumps(presence).encode('utf-8'))
    data = s.recv(1000000)
    data = json.loads(data)
    print('Сообщение от сервера: ', data)
    s.close()

if __name__ ==  '__main__':
    main()