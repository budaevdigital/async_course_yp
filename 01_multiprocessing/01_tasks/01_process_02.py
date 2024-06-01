import time
from multiprocessing import Process, current_process


def custom_func():
    proc_name = current_process().name
    proc_pid = current_process().pid
    print(f"Запустился процесс {proc_name}[{proc_pid}]")
    time.sleep(2)
    print(f"Завершился процесс {proc_name}[{proc_pid}]")


if __name__ == "__main__":
    p1 = Process(name="Job-1", target=custom_func)
    proc_pid = p1.pid
    proc_status = p1.is_alive()
    print(f"Процесс с pid[{proc_pid}] работает[{proc_status}]")

    p1.start()
    proc_status = p1.is_alive()
    proc_pid = p1.pid
    print(f"Процесс с pid[{proc_pid}] работает[{proc_status}]")
    p1.join()

    proc_status = p1.is_alive()
    print(f"Процесс с pid[{proc_pid}] работает[{proc_status}]")