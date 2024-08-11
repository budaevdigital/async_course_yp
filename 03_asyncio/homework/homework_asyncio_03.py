import asyncio
import datetime

clients = set()  # Множество для хранения активных подключений


async def handle_client(reader, writer):
    address = writer.get_extra_info('peername')
    clients.add(writer)
    print(f"Клиент {address} подключился.")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break

            # Отправляем статус всем клиентам
            await send_status()

    except asyncio.CancelledError:
        pass
    finally:
        print(f"Клиент {address} отключился.")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()


async def send_status():
    status = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Подключено клиентов: {len(clients)}\n"
    print(f"Отправка статуса: {status.strip()}")
    for writer in clients:
        writer.write(status.encode())
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
