import socket


HOST, PORT = "127.0.0.1", 8000


def send_message():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        # sock.sendall(b"Hello world!")
        sock.sendall(b"time")
        # sock.close()
        data = sock.recv(1024)
    print(f"Передано: {data}")


if __name__ == '__main__':
    send_message()
