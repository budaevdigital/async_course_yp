from multiprocessing import Pool, Queue, Manager


def worker(item: tuple[Queue, int]):
    queue, index = item
    queue.put(index)
    print(f'{index} элемент отправлен в очередь')


if __name__ == '__main__':
    m = Manager()
    queue = m.Queue()
    items = [(queue, 1), (queue, 2), (queue, 3)]
    with Pool() as pool:
        pool.map(worker, items)
