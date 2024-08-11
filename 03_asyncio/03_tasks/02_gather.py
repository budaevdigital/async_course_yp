import asyncio
import time


async def greeting(name: str) -> None:
    print(f"{time.ctime()} - Привет {name} ...")
    await asyncio.sleep(2)
    print(f"{time.ctime()} - Пока {name}!")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [greeting(name) for name in ("Гость", "Пользователь")]-
    group_task = asyncio.gather(*tasks, return_exceptions=True)
    try:
        loop.run_until_complete(group_task)
    finally:
        loop.close()
