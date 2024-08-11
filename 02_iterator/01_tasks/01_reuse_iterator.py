

# итерабельный объект
class IterableObject:
    def __init__(self, stop_value: int):
        self.current_value = -1
        self.stop_value = stop_value - 1

    def __iter__(self):
        return Iterator(self)


# итератор
class Iterator:
    def __init__(self, iterable_object: IterableObject):
        self.iterable_object = iterable_object

    def __next__(self):
        if self.iterable_object.current_value < self.iterable_object.stop_value:
            self.iterable_object.current_value += 1
            return self.iterable_object.current_value
        self.iterable_object.current_value = -1  # без обновления счетчика - повторная итерация будет невозможна
        raise StopIteration


# В Python возможно создать и итерабельный объект и итератор вместе
class IteratorAndObject:
    def __init__(self, stop_value: int):
        self.current_value = -1
        self.stop_value = stop_value - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_value < self.stop_value:
            self.current_value += 1
            return self.current_value
        self.current_value = -1
        raise StopIteration


# экземпляр раздельного итератора
iter_check_one = IterableObject(5)

for count in iter_check_one:
    print(count)

for count in iter_check_one:
    print(count)

# экземпляр общего итератора и итерабельного объекта
iter_check_two = IteratorAndObject(5)

for count in iter_check_two:
    print(count)


# ------------

# Интересный вопрос связанный с итератором

digits = iter(range(100, 300))
print(150 in digits)
# под "капотом" через __next__ досчитает до нужного значения 150 и на нем остановится!
# дальше продолжит проверять на равенство (120 == ...) со значения 151 и до конца!
# после одной полной итераций повторно проитерироваться не получится
# и дальше будет везде False
print(120 in digits)
print(55 in digits)
print(240 in digits)
