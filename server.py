from socket import *
import time
import json
import argparse
import select
from logs.server_log_config import log,logger

@log
def pars_arg():
    parser = argparse.ArgumentParser(description='ip, port')
    parser.add_argument("-p", dest='port', default=7777, type=int)
    parser.add_argument("-a", dest='ip', default='')
    args = parser.parse_args()
    return args.port, args.ip


def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов"""
    responses = {} # Словарь ответов сервера вида {сокет: запрос}
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)
    return responses


def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """
    for sock in w_clients:
        if sock in requests:
            try:
                # Подготовить и отправить ответ сервера
                resp = requests[sock].upper().encode('utf-8')
                # Эхо-ответ сделаем чуть непохожим на оригинал
                sock.send(resp)
            except: # Сокет недоступен, клиент отключился
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)

@log
def mainloop(ip, port):
    """ Основной цикл обработки запросов клиентов"""
    address = (ip, port)
    clients = []
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)  # Таймаут для операций с сокетом
    while True:
        try:
            conn, addr = s.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print(f"Получен запрос на соединение от {addr}")
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 1
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился
            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                write_responses(requests, w, clients)  # Выполним отправку ответов



def main_func():
    port, ip = pars_arg()
    mainloop(ip, port)



if __name__ ==  '__main__':
    try:
        main_func()
    except Exception as e:
        logger.critical(f'Не предвиденная ошибка {e}')