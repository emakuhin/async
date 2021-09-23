from socket import *
import json
import time
import argparse
from logs.client_log_config import log




presence = {
"action": "presence",
"time": '',
"type": "status",
"user": {
"account_name": "Makuhin",
"message": "Hello, I am here!"}
}

@log
def pars_arg():
    parser = argparse.ArgumentParser(description='ip, port')
    parser.add_argument("-p", dest='port', default=7777, type=int)
    parser.add_argument("-a", dest='ip', default='localhost')
    args = parser.parse_args()
    return args.port, args.ip

@log
def client(port, ip):

    with socket(AF_INET, SOCK_STREAM) as sock:# Создать сокет TCP
        sock.connect((ip, port)) # Соединиться с сервером
        while True:
            message = input('Введите сообщение: ')
            if message == 's':
                break
            elif message == 'read':
                data = sock.recv(1000000)
                data = json.loads(data)
                print('Сообщение от сервера: ', data)
            else:
                presence['time'] = time.time()
                presence['user']['message'] = message
                sock.send(json.dumps(presence).encode('utf-8'))



def main_func():
    try:
        port, ip = pars_arg()
        client(port, ip)
    except Exception as e:
        print(e)
#        log.critical(f'Не предвиденная ошибка {e}')




if __name__ ==  '__main__':
    main_func()