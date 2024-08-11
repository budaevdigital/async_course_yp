import asyncio


async def test_coroutine(index: int, name_method: str):
    await asyncio.sleep(1)
    print(f"Iterable position >> {index} in method: {name_method}")


async def init_task_create_task():
    print("In create task method")
    loop = asyncio.get_event_loop()
    for index in range(5):
        loop.create_task(test_coroutine(index, "create_task"))
        await asyncio.sleep(0)  # для переключения контекста в момент итерации


async def init_task_ensure_future():
    print("In ensure future")
    for index in range(5, 10):
        asyncio.ensure_future(test_coroutine(index, "ensure_future"))
        await asyncio.sleep(0)


async def check_eventloop():
    loop = asyncio.get_event_loop()
    loop_2 = asyncio.get_event_loop()

    print(f"ID for loop - {id(loop)}")
    print(f"ID for loop - {id(loop_2)}")
    print(f"loop is equal to loop_2 - {loop is loop_2}")


async def main():
    loop = asyncio.get_event_loop()  # получаем существующий цикл событий

    loop.create_task(check_eventloop())
    loop.create_task(init_task_create_task())
    loop.create_task(init_task_ensure_future())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()  # создаем цикл событий
    print(f"ID for loop on start app - {id(loop)}")
    loop.run_until_complete(main())

    pending_tasks = asyncio.all_tasks(loop)
    tasks_before_closing = asyncio.gather(*pending_tasks, return_exceptions=True)
    loop.run_until_complete(tasks_before_closing)

    loop.close()
    print("Event loop closed")
