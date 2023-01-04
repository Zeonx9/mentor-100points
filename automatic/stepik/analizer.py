from math import ceil
from collections import namedtuple

DataRow = namedtuple('DataRow', ['name', 'scores'])

file_name = input('Enter the name of file (.csv): ')
if not file_name:
    file_name = "data.csv"
file_name = file_name.replace("\\", "/").replace('"', "")

with open(file_name, "r", encoding="UTF-8") as file, open("id_list.txt") as s_id:
    lines = file.readlines()
    raw_data = [line.replace(", ", " ").replace('"', "").split(",") for line in lines]
    ordered_ids = [int(line) for line in s_id.readlines()]

if file_name != "data.csv":
    with open("data.csv", "w", encoding="UTF-8") as file:
        file.writelines(lines)


headers = [' '.join(h.split()[:-1]) for h in raw_data[0][3:-8]]
short_headers = {}
for i, h in enumerate(headers):
    if h not in short_headers:
        short_headers[h] = [i, 1]
    else:
        short_headers[h][1] += 1

# print(short_headers)

data = {
    int(row[0]): DataRow(' '.join(row[1:3]), [ceil(float(val)) for val in row[3:-8]])
    for row in raw_data[1:]
}

grouped_data = [[0] * len(short_headers) for _ in range(len(ordered_ids))]
for i, key in enumerate(ordered_ids):
    if key not in data:
        continue
    grouped_data[i] = [sum(data[key].scores[st:st + count]) for st, count in sorted(short_headers.values())]


def webinar(n):
    if n < 17:
        return 3 * (n - 11), 3
    if 17 <= n <= 18:
        return 2 * (n - 17) + 18, 2
    if n == 19:
        return 0, 0
    return 3 * (n - 20) + 22, 3


def task_request():
    web_num = int(input('Enter webinar number: '))
    while web_num >= 0:
        web_st, web_c = webinar(web_num)
        print(*list(short_headers.keys())[web_st:web_st + web_c])
        for i, idd in enumerate(ordered_ids):
            prnt_str = '\t'.join(map(lambda x: str(x) if x > 0 else ' ', grouped_data[i][web_st:web_st + web_c]))
            print(prnt_str)
        web_num = int(input('Enter next webinar number: '))


def student_request():
    stud = int(input('Paste the id: '))
    while stud in ordered_ids:
        stud = ordered_ids.index(stud)
        prnt_str = '\t'.join(map(lambda x: str(x) if x > 0 else ' ', grouped_data[stud]))
        print(prnt_str)
        stud = int(input('Paste next the id: '))


if __name__ == "__main__":
    req = input("Enter\n"
                "'task' to print marks for the task or\n"
                "'student' to print all marks of that student\n")

    if req == 'task':
        task_request()
    elif req == 'student':
        student_request()
    else:
        print('NO SUCH REQUEST')
