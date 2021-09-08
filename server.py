from socket import *
import time
import json
import argparse

parser = argparse.ArgumentParser(description='ip, port')
parser.add_argument("-p", dest='port', default=7777, type=int)
parser.add_argument("-a", dest='ip', default='')
args = parser.parse_args()
port,ip = args.port, args.ip

s = socket(AF_INET, SOCK_STREAM) # Создает сокет TCP
s.bind((ip, port)) # Присваивает порт 8888
s.listen(5) #

response_200 = {"response": 200, "alert":"Ok"}

def main():
    while True:
        client, addr = s.accept()
        data = client.recv(1000000)
        data = json.loads(data)
        if data:
            client.send(json.dumps(response_200).encode('utf-8'))
        time_client = time.ctime(data['time'])
        print('Сообщение: ', data, ', было отправлено клиентом: ',addr)
        msg = f'Привет, клиент. Время вашего обращения {time_client}'
        client.send(msg.encode('utf-8'))
        client.close()


if __name__ ==  '__main__':
    main()