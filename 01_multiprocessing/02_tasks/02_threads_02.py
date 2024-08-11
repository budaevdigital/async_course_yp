"""
Реализуйте методы f1 и f2.

Опишите их логику работы с пулом потоков для возведения в квадрат последовательности,
а также подсчёта суммы её элементов.
"""
from concurrent.futures import ThreadPoolExecutor

data = range(1, 10)
pool_size = 5


def f1(item):
    # Возведение в квадрат
    return item ** 2


def f2(data):
    # Подсчёт суммы элементов массива
    return sum(data)


def worker(data):
    """
    Возведение всех элементов массива в квадрат и
    подсчёт суммы всех элементов
    """
    result = 0
    with ThreadPoolExecutor(max_workers=pool_size) as pool:
        # Взаимодействие с пулом для возведения в квадрат и подсчёта суммы всех элементов
        list_numbers = list(pool.map(f1, data))
        result += pool.submit(f2, list_numbers).result()
    return result


if __name__ == "__main__":
    print(worker(data))
