import asyncio
import time


async def greeting(name: str) -> None:
    print(f"{time.ctime()} - Привет {name} ...")
    await asyncio.sleep(2)
    print(f"{time.ctime()} - Пока {name}!")
    loop = asyncio.get_event_loop()
    loop.stop()  # явно останавливаем цикл событий


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(greeting("Гость"))
    loop.create_task(greeting("Пользователь"))
    try:
        loop.run_forever()
    finally:
        loop.close()
