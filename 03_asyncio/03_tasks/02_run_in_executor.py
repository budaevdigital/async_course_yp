import time
import asyncio


async def greeting(name: str):
    print(f'{time.ctime()} Привет, {name}...')
    await asyncio.sleep(1.6)
    print(f'{time.ctime()} Пока, {name}...')


def blocking_sleep():
    time.sleep(0.7)
    print(f'{time.ctime()} Вызов блокирующего метода в отдельном потоке...')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(greeting("Гость"))
    loop.create_task(greeting("Пользователь"))
    loop.create_task(greeting("Еще кто-то"))
    loop.run_in_executor(None, blocking_sleep)
    pending_task = asyncio.all_tasks(loop)
    group_task = asyncio.gather(*pending_task, return_exceptions=True)
    loop.run_until_complete(group_task)
    loop.close()
