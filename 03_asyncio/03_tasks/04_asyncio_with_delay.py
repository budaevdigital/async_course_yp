import random
import asyncio


async def delay():
    rand_delay = random.uniform(0.5, 4.5)
    print(f'Сгенерировано число {rand_delay}...')
    await asyncio.sleep(rand_delay)
    print(f'Завершилась корутина {rand_delay}...')
    return rand_delay


async def main():
    tasks = [asyncio.create_task(delay()) for _ in range(5)]
    print("Начало работы")
    # wait не отменяет задачи как wait_for, а приостанавливает их
    # return_when = FIRST_COMPLETED or FIRST_EXCEPTION or ALL_COMPLETED
    done_tasks, pending_tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    print(pending_tasks)
    print(done_tasks)

    print("Результаты работы приложения", done_tasks.pop().result())

    # отменяем ожидающие задачи, чтобы не было ошибок при заверщении
    for task in pending_tasks:
        task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
