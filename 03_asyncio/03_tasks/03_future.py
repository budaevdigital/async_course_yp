import asyncio


async def test_coroutine():
    print("Start coro")
    await asyncio.sleep(3)


async def main():
    loop = asyncio.get_event_loop()
    task = loop.create_task(test_coroutine())
    print(type(task))
    print(task.done())

    my_future = asyncio.Future()
    print(type(my_future))
    print(my_future.done())
    my_future.set_result("Результат")
    print(my_future.done())  # Теперь Future завершена
    print(my_future.result())

if __name__ == "__main__":
    asyncio.run(main())





