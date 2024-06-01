import time
from multiprocessing import Process, Pipe


def producer_send(conn: Pipe):
    conn.send(['Привет', None, 256])
    conn.close()
    time.sleep(2)


def consumer_get(conn: Pipe):
    value = conn.recv()
    print(value)
    time.sleep(3)


if __name__ == '__main__':
    producer, consumer = Pipe()

    p_prod = Process(target=producer_send, args=(producer,))
    p_cons = Process(target=consumer_get, args=(consumer,))

    p_prod.start()
    p_cons.start()

    p_prod.join()
    p_cons.join()
