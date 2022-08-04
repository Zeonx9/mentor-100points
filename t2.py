# задача 8.2

from itertools import product


s1 = 'ЗАБИВ'
s2 = 'ШМОТ'
w1 = {}
w2 = {}

for i in range(len(s1)):
    w1[s1[i]] = i  # добавляем пару буква-номер в словарь

for i in range(len(s2)):
    w2[s2[i]] = i

passwords = []
for x in product('ЗАБИВ', repeat=3):  # пробегаемся по первому слову и выбиарем все возможные тройки
    if w1[x[0]] < w1[x[1]] < w1[x[2]]:  # проверка на порядок
        for y in product('ШМОТ', repeat= 3):  # аналогично для 2ого слова
            if w2[y[0]] < w2[y[1]] < w2[y[2]]:
                passwords.append(x + y)

print(len(passwords))


