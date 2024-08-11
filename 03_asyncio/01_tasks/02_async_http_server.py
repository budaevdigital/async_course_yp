import socket

HOST, PORT = "0.0.0.0", 8888

PORTS = [22, 23, 80, 443, 3000, 8000, 8001, 8888, 9000]


def request_handle(request: bytes) -> bytes:
    request_data = request.decode()
    http_response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n{request_data}"""
    return http_response.encode()


def scanner_ports(ports: list[int]) -> None:
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            res = sock.connect_ex((HOST, port))
            print(f"{port}: {res}")


def server_forever():
    # Устанавливаем TCP соединение для обмена данными между процессом-клиентом и процессом-сервером
    # сокет инкапсулируют всю логику работы с сетью и передачей пакетов данных
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        # включение функции переиспользования портов (если не хватит стандартного объема - 65 535)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        listen_socket.bind((HOST, PORT))
        listen_socket.listen()  # переводим сокет в режим прослушки
        listen_socket.setblocking(False)  # делаем сокет неблокирующим, чтобы обрабатывать больше запросов
        print(f"Прослушивается порт {PORT} ...")

        while True:
            client_connection, client_address = listen_socket.accept()
            print(f"{client_connection=} | {client_address=}")
            with client_connection:
                request = client_connection.recv(1024)  # Получаем информацию от клиента пачками по 1024 байт
                print(f"{request=}")
                http_response = request_handle(request)
                print(f"{http_response=}")
                client_connection.sendall(http_response)


if __name__ == '__main__':
    # scanner_ports(PORTS)
    server_forever()
