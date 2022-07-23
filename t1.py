from itertools import product

nicks = []
for x in product('ЧЕЛЯДЬ', repeat=5):  # пройтись по всем возможным комбинациям из этих букв длины 5
    s = ''.join(x)                     # привести кортеж к строке для удобства работы
    if 'ЕЬ' not in s and 'ЯЬ' not in s and s.count('Е') + s.count('Я') == 2:
        nicks.append(s)                # взять прозвища удовлетворяющие условиям

print(len(nicks))


#  однострочный вариант решения
print(len(list(filter(lambda t: 'ЕЬ' not in t and 'ЯЬ' not in t and t.count('Е') + t.count('Я') == 2,
                      map(lambda s: ''.join(s), product('ЧЕЛЯДЬ', repeat=5))))))


