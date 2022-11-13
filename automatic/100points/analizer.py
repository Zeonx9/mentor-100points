from collections import namedtuple

DataTemplate = namedtuple('DataTemplate', ['name', 'task', 'score'])

with open("data.csv", "r", encoding="UTF-8") as file, \
     open("name_list.txt", encoding="UTF-8") as name_file:
    raw_data = [DataTemplate(*line.split(",")) for line in file.readlines()]
    ordered_names = [line.strip() for line in name_file.readlines()]

people_dict: dict[str, dict[str, int]] = {}
tasks_dict: dict[str, int] = {}
for row in raw_data:
    if row.name not in people_dict:
        people_dict[row.name] = {}

    people_dict[row.name][row.task] = int(row.score)

    if row.task not in tasks_dict:
        tasks_dict[row.task] = len(tasks_dict)


data = [[0] * len(tasks_dict) for _ in range(len(ordered_names))]
for i, name in enumerate(ordered_names):
    if name not in people_dict:
        continue

    for k, t in enumerate(tasks_dict):
        if t in people_dict[name]:
            data[i][k] = people_dict[name][t]

# print(*tasks_dict.items())
# for i in range(len(ordered_names)):
#     print(ordered_names[i], data[i])

web_name = input('Enter webinar number: ')

all_columns = [(ind, task.split()) for task, ind in tasks_dict.items()]
columns = [tup for tup in all_columns if all(key in tup[1] for key in web_name.split())]
columns.sort(key=lambda tup: ['Базовый', 'Средний', 'Сложный'].index(tup[1][-1]))
indices = [tup[0] for tup in columns]

print(*[' '.join(c[1]) for c in columns])
for i in range(len(ordered_names)):
    print('\t'.join(map(lambda e: str(e) if e > 0 else ' ', [data[i][j] for j in indices])))
