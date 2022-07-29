# задача 8.1

from itertools import product

nicks = []
for x in product('МЕЛОЧЬ', repeat=5):  # пройтись по всем возможным комбинациям из этих букв длины 5
    s = ''.join(x)                     # привести кортеж к строке для удобства работы
    if 'ЕЬ' not in s and 'ОЬ' not in s and s.count('Е') + s.count('О') == 2:
        nicks.append(s)                # взять прозвища удовлетворяющие условиям

print(len(nicks))


#  однострочный вариант решения
print(len(list(filter(lambda t: 'ЕЬ' not in t and 'ОЬ' not in t and t.count('Е') + t.count('О') == 2,
                      map(lambda s: ''.join(s), product('МЕЛОЧЬ', repeat=5))))))


