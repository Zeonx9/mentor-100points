from collections import namedtuple
from scraper import main_routine as scrape

DataTemplate = namedtuple('DataTemplate', ['name', 'task', 'score', 'max_score'])


def sort_and_analyze_data():
    with open("data.csv", "r", encoding="UTF-8") as file, \
         open("name_list.txt", encoding="UTF-8") as name_file:
        raw_data = [DataTemplate(*line.split(",")) for line in reversed(file.readlines())]
        ordered_names = [line.strip() for line in name_file.readlines()]

    people_dict: dict[str, dict[str, int]] = {}
    tasks_dict: dict[str, int] = {}
    max_scores: dict[str, int] = {}
    for row in raw_data:
        if row.name not in people_dict:
            people_dict[row.name] = {}

        people_dict[row.name][row.task] = int(row.score)

        if row.task not in tasks_dict:
            tasks_dict[row.task] = len(tasks_dict)

        max_scores[row.task] = row.max_score

    data = [[-1] * len(tasks_dict) for _ in range(len(ordered_names))]
    for i, name in enumerate(ordered_names):
        if name not in people_dict:
            continue

        for t, k in tasks_dict.items():
            if t in people_dict[name]:
                data[i][k] = people_dict[name][t]

    return data, ordered_names, tasks_dict, max_scores


def get_slice_indices(tasks_dict, max_scores, web_name):
    all_columns = [(ind, task.split()) for task, ind in tasks_dict.items()]
    columns = [tup for tup in all_columns if all(key in tup[1] for key in web_name.split())]
    columns.sort(key=lambda tup: ['Базовый', 'Средний', 'Сложный'].index(tup[1][-1]))
    indices = [tup[0] for tup in columns]
    names = [' '.join(t[1]) for t in columns]
    maximums = [max_scores[n].strip() for n in names]
    return names, indices, maximums


def print_home_work_result(web_name):
    data, ordered_names, tasks_dict, max_scores = sort_and_analyze_data()
    names, indices, maximums = get_slice_indices(tasks_dict, max_scores, web_name)

    print(*names)
    print("max", *maximums)
    for i in range(len(ordered_names)):
        print('\t'.join(map(lambda e: ' ' if e < 0 else str(e), [data[i][j] for j in indices])))


def prepare_output_for_parser(out_file_name: str, homework: str, update=False):
    def deal_with_absent_works(res: int) -> str:
        return '-1' if res < 0 else str(res)

    if update:
        scrape("update")

    data, ordered_names, tasks_dict, max_scores = sort_and_analyze_data()
    names, indices, maximums = get_slice_indices(tasks_dict, max_scores, homework)

    out_lines = [','.join(maximums) + '\n']
    for i in range(len(ordered_names)):
        line = ordered_names[i] + ','
        line += ','.join(map(deal_with_absent_works, [data[i][j] for j in indices]))
        out_lines.append(line + '\n')

    with open(out_file_name, 'w', encoding='UTF-8') as out_file:
        out_file.writelines(out_lines)


if __name__ == "__main__":
    should_update = input("update?").lower()
    if should_update == "yes" or should_update == "y":
        scrape("update")

    web = input('Enter webinar number: ')
    print_home_work_result(web)

    prepare_output_for_parser(f"out_data_{web}.csv", web)
