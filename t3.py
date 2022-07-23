from itertools import product

# словари содержащие номера букв в словах
w1 = {x: i for i, x in enumerate('ЗАБИВ')}
w2 = {x: i for i, x in enumerate('ШМОТ')}

passwords = []
for x in product('ЗАБИВ', repeat=3):  # пробегаемся по первому слову и выбиарем все возможные тройки
    if w1[x[0]] < w1[x[1]] < w1[x[2]]:  # проверка на порядок и за одно на несовпадение
        for y in product('ШМОТ', repeat= 3):  # аналогично для 2ого слова
            if w2[y[0]] < w2[y[1]] < w2[y[2]]:
                passwords.append(x + y)  # добавляем слово прошедшее отбор

print(len(passwords))


