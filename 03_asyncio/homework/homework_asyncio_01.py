"""
Реализуйте работу цикла событий и перехватите системные вызовы `SIGINT` и `SIGTERM`
для корректного завершения работы.

Используйте метод `add_signal_handler()` и модуль `signal`.
"""

import asyncio
import signal
import logging
import random
import functools
from datetime import datetime

logging.basicConfig(
    format="%(module)s : %(funcName)s : (Process Details : (%(process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s))\nLog Message : %(message)s\n",
    datefmt="%d-%B,%Y %I:%M:%S %p",
    level=logging.INFO
)

NAME_SIGNALS = ("SIGINT", "SIGTERM")


def handler_signals(sig_name: str, loop: asyncio.AbstractEventLoop) -> None:
    logging.info(f"Сигнал: '{sig_name}' получен @ {datetime.now()}")
    # при отлове хендлером сигнала, оотменяем и останавливаем текущие задачи
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.stop()


async def set_handler_signals(loop: asyncio.AbstractEventLoop) -> None:
    print(f"Установка сигналов {NAME_SIGNALS}")
    for sig_name in NAME_SIGNALS:
        loop.add_signal_handler(getattr(signal, sig_name), functools.partial(handler_signals, sig_name, loop))


async def delay() -> float:
    rand_delay = random.uniform(0.5, 4.5)
    print(f'Сгенерировано число {rand_delay}...')
    await asyncio.sleep(rand_delay)
    print(f'Завершилась корутина {rand_delay}...')
    return rand_delay


async def start() -> None:
    loop = asyncio.get_event_loop()
    await set_handler_signals(loop)
    print("Программа запущена. Ожидание завершения...")
    await delay()


def main():
    logging.info(f"Старт: {datetime.now()}")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start())
        loop.run_forever()
    except asyncio.CancelledError:
        pass
    finally:
        # Закрываем все оставшиеся задачи перед закрытием цикла
        pending_tasks = asyncio.all_tasks(loop)
        if pending_tasks:
            loop.run_until_complete(asyncio.gather(*pending_tasks, return_exceptions=True))
        loop.close()
        logging.info(f"Завершено: {datetime.now()}")


if __name__ == "__main__":
    main()
