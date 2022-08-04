# задача 8.3

from itertools import product

codes = []

for length in range(2, 7):
    for x in product('ЛУЧШАЯ', repeat=length):   # состовляем все кобинации нужной длины из исходного набора
        # проверка на повторы
        if len(set(x)) == length:
            codes.append(x)


# количество умножаем на 10
print(len(codes) * 10)



