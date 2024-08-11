from multiprocessing import Process


class Worker(Process):
    def __init__(self, func, func_args, queue):
        super().__init__()
        self.queue = queue
        self.func = func
        self.func_args = func_args

    def run(self):
        value = self.func(*self.func_args)
        self.queue.put(value)
