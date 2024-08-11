import typing


class CyclicIterator:
    def __init__(self, sequence: typing.Sequence):
        self.current_count = 0
        self.sequence = sequence

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_count >= len(self.sequence):
            self.current_count = 0
        result = self.sequence[self.current_count]
        self.current_count += 1
        return result


def main():
    cyclic_iterator = CyclicIterator(range(3))

    for i in cyclic_iterator:
        print(i)


if __name__ == "__main__":
    main()
