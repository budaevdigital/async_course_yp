import datetime
import logging
import selectors
import socket
import sys

HOST, PORT = "0.0.0.0", 8000

PORTS = [22, 23, 80, 443, 3000, 8000, 8001, 8888, 9000]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


def new_connection(selector: selectors.BaseSelector, sock: socket.socket):
    new_conn, address = sock.accept()
    logger.info(f"Принято новое соединение {new_conn}, {address}")
    new_conn.setblocking(False)  # делаем сокет неблокирующим, чтобы обрабатывать больше запросов
    selector.register(new_conn, selectors.EVENT_READ, read_callback)


def read_callback(selector: selectors.BaseSelector, sock: socket.socket):
    if data := sock.recv(1024):
        message = data.decode()
        logger.info(f"Данные от клиента: {message}")
        sock.send(data)
        if message == "time":
            print(datetime.datetime.now())
    else:
        logger.info(f"Закрытие соединения")
        selector.unregister(sock)
        sock.close()


# забираем все эвенты в OC и достаем метод для обработки
def run_iteration(selector: selectors.BaseSelector):
    events = selector.select()
    for key, mask in events:
        callback = key.data
        callback(selector, key.fileobj)


def server_forever():
    with selectors.SelectSelector() as selector:
        # Устанавливаем TCP соединение для обмена данными между процессом-клиентом и процессом-сервером
        # сокет инкапсулируют всю логику работы с сетью и передачей пакетов данных
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
            # включение функции переиспользования портов (если не хватит стандартного объема - 65 535)
            listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            listen_socket.bind((HOST, PORT))
            listen_socket.listen()  # переводим сокет в режим прослушки
            listen_socket.setblocking(False)  # делаем сокет неблокирующим, чтобы обрабатывать больше запросов
            logger.info(f"Прослушивается порт {PORT} ...")

            # Зарегистрировать каждое событие получения новых данных по серверному сокету и вызвать функцию `new_connection`
            selector.register(listen_socket, selectors.EVENT_READ, new_connection)

            while True:
                try:
                    run_iteration(selector)
                except ConnectionResetError:
                    print("ConnectionResetError")


if __name__ == '__main__':
    # запуск echo-сервера
    server_forever()
