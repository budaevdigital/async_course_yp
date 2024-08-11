import asyncio
import datetime

clients = set()  # Множество для хранения активных подключений


async def handle_client(reader, writer):
    address = writer.get_extra_info('peername')
    clients.add(writer)
    print(f"Клиент {address} подключился.")
    last_activity = datetime.datetime.now()

    async def monitor_inactivity():
        nonlocal last_activity
        while True:
            await asyncio.sleep(1)
            now = datetime.datetime.now()
            if (now - last_activity).total_seconds() > 10:
                print(f"Клиент {address} отключен из-за неактивности.")
                writer.write("Вы были отключены из-за неактивности.\n".encode('utf-8'))
                await writer.drain()
                if writer in clients:
                    clients.remove(writer)
                writer.close()
                await writer.wait_closed()
                break
            elif (now - last_activity).total_seconds() > 5:
                print(f"Клиент {address} неактивен 5 секунд, отправка предупреждения.")
                writer.write("Вы неактивны в течение 5 секунд. Пожалуйста, продолжайте работу.\n".encode('utf-8'))
                await writer.drain()

    inactivity_task = asyncio.create_task(monitor_inactivity())

    try:
        while True:
            try:
                data = await asyncio.wait_for(reader.read(100), timeout=10.0)
                if not data:
                    break
                last_activity = datetime.datetime.now()
                # Отправляем статус всем клиентам
                await send_status()
            except asyncio.TimeoutError:
                continue
    except asyncio.CancelledError:
        pass
    finally:
        print(f"Клиент {address} отключился.")
        if writer in clients:
            clients.remove(writer)
        writer.close()
        await writer.wait_closed()
        inactivity_task.cancel()


async def send_status():
    status = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Подключено клиентов: {len(clients)}\n"
    print(f"Отправка статуса: {status.strip()}")
    for writer in clients:
        writer.write(status.encode('utf-8'))
        await writer.drain()


async def status_updater():
    while True:
        await send_status()
        await asyncio.sleep(2)


async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Сервер запущен на {addr}")

    async with server:
        await asyncio.gather(
            server.serve_forever(),
            status_updater(),
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Сервер остановлен.")
