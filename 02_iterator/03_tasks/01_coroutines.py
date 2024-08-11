def hello():
    value = yield "Hello"
    print(f"Get value = {value}")


def main():
    coro = hello()

    value = next(coro)
    print(value)  # вернет "Hello" от корутины hello()

    coro.send("11")  # отправляет значение в yeild на 2 строчке hello()

    next(coro)
    # Вызовет исключение StopIter


if __name__ == '__main__':
    main()
