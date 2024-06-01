from multiprocessing import Process, Queue
from time import sleep


def produce(queue: Queue):
    while True:
        message = 'ping'
        queue.put(message)
        sleep(1)


def consume(queue: Queue):
    while message := queue.get():
        print(message)


if __name__ == '__main__':
    queue = Queue()
    producer = Process(target=produce, args=(queue,))
    consumer = Process(target=consume, args=(queue,))
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()

