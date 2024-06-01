from multiprocessing import Process, Queue
import random
import time


class Producer(Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        for idx in range(5):
            item = random.randint(0, 100)
            self.queue.put(item)
            print(f'Producer: запись {item} добавлена {self.name}\n')
            time.sleep(1)


class Consumer(Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                print('Очередь пуста')
                break
            else:
                time.sleep(1)
                item = self.queue.get()
                print(f'Consumer: запись {item} получена из {self.name} \n')
                time.sleep(1)


if __name__ == '__main__':
    queue = Queue()
    process_producer = Producer(queue)
    process_consumer = Consumer(queue)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
