def func(from_, to=10, step=1):
    for idx in range(from_, to, step):
        yield idx
        return idx
    return -1


def main():
    f = func(2, -5, -2)
    print(next(f))
    print(next(f))
    f.close()
    print(next(f))


if __name__ == '__main__':
    main()