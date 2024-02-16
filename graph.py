import os
import matplotlib.pyplot as plt
from database import read_data
from functools import wraps
from typing import Callable


def graph_template(graph: Callable) -> Callable:
    @wraps(graph)
    def wrapper(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
        fig, ax = plt.subplots()
        ax.grid(which='major', color='k')
        ax.minorticks_on()
        ax.grid(which='minor', color='gray', linestyle=':')
        plt.grid(True)
        fig.set_size_inches(11, 6.5)
        graph(data)
        plt.close()
    return wrapper


@graph_template
def views(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
    plt.title('Количество просмотров')
    plt.ylabel('Просмотры')
    for i in range(10):
        plt.plot([d[0]['date'].split()[1] for d in data], [d[i]['views_count'] for d in data])
    plt.legend([f'{data[0][i]["name"]}' for i in range(10)], loc=1)
    plt.savefig('output\\' + name_filter('views.png'), dpi=100)


@graph_template
def average_score(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
    plt.title('Сравнительная средняя оценка')
    plt.ylabel('Балл')
    for i in range(10):
        plt.plot([d[0]['date'].split()[1] for d in data], [d[i]['average_score'] for d in data])
    plt.legend([f'{data[0][i]["name"]}' for i in range(10)], loc=1)
    plt.savefig('output\\' + name_filter('average score.png'))


@graph_template
def ratings_count(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
    plt.title('Количество оценок')
    plt.ylabel('Оценки')
    for i in range(10):
        plt.plot([d[0]['date'].split()[1] for d in data], [d[i]['ratings_count'] for d in data])
    plt.legend([f'{data[0][i]["name"]}' for i in range(10)], loc=1)
    plt.savefig('output\\' + name_filter('ratings count.png'))


def scores(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
    for i in range(10):
        fig, ax = plt.subplots()
        ax.grid(which='major', color='k')
        ax.minorticks_on()
        ax.grid(which='minor', color='gray', linestyle=':')
        plt.grid(True)
        fig.set_size_inches(11, 6.5)
        plt.title(f'Оценки {data[0][i]["name"]}')
        plt.ylabel('Оценки')
        for j in range(10):
            plt.plot([d[0]['date'].split()[1] for d in data], [d[i]['ratings'][j] for d in data])
        plt.legend([10 - i for i in range(10)], loc=1)
        plt.savefig('output\\' + name_filter(f'scores {data[0][i]["name"]}.png'))
        plt.close()


def scores_in_percent(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
    for i in range(10):
        fig, ax = plt.subplots()
        ax.grid(which='major', color='k')
        ax.minorticks_on()
        ax.grid(which='minor', color='gray', linestyle=':')
        plt.grid(True)
        fig.set_size_inches(11, 6.5)
        plt.title(f'Оценки (%) {data[0][i]["name"]}')
        plt.ylabel('Оценки')
        for j in range(10):
            plt.plot([d[0]['date'].split()[1] for d in data],
                     [d[i]['ratings'][j]*100/d[i]['ratings_count'] for d in data])
        plt.legend([10 - i for i in range(10)], loc=1)
        plt.savefig('output\\' + name_filter(f'scores in percent {data[0][i]["name"]}.png'))
        plt.close()


@graph_template
def views_increase(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
    plt.title('Прирост просмотров')
    plt.ylabel('Просмотры')
    for i in range(10):
        plt.plot([d[0]['date'].split()[1] for d in data][1::2],
                 [data[j + 1][i]['views_count'] - data[j][i]['views_count'] for j in range(len(data) - 1)][::2])
    plt.legend([f'{data[0][i]["name"]}' for i in range(10)], loc=1)
    plt.savefig('output\\' + name_filter('views increase.png'))


@graph_template
def average_score_increase(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
    plt.title('Изменение средней оценки')
    plt.ylabel('Средняя оценка')
    for i in range(10):
        plt.plot([d[0]['date'].split()[1] for d in data][1::2],
                 [data[j + 1][i]['average_score'] - data[j][i]['average_score'] for j in range(len(data) - 1)][::2])
    plt.legend([f'{data[0][i]["name"]}' for i in range(10)], loc=1)
    plt.savefig('output\\' + name_filter('average score increase.png'))


@graph_template
def ratings_count_increase(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
    plt.title('Прирост количества оценок')
    plt.ylabel('Количество оценок')
    for i in range(10):
        plt.plot([d[0]['date'].split()[1] for d in data][1::2],
                 [[data[j + 1][i]['ratings_count'] - data[j][i]['ratings_count']
                   for i in range(10)] for j in range(len(data) - 1)][::2])
    plt.legend([f'{data[0][i]["name"]}' for i in range(10)], loc=1)
    plt.savefig('output\\' + name_filter('ratings count increase.png'))


def scores_increase(data: list[list[dict[str, str | int | float | list[int]]]]) -> None:
    for i in range(10):
        fig, ax = plt.subplots()
        ax.grid(which='major', color='k')
        ax.minorticks_on()
        ax.grid(which='minor', color='gray', linestyle=':')
        plt.grid(True)
        fig.set_size_inches(11, 6.5)
        plt.title(f'Прирост оценок {data[0][i]["name"]}')
        plt.ylabel('Количество оценок')
        for j in range(10):
            plt.plot([d[0]['date'].split()[1] for d in data][1::2],
                     [data[k + 1][i]['ratings'][j] - data[k][i]['ratings'][j] for k in range(len(data) - 1)][::2])
        plt.legend([10 - j for j in range(10)], loc=1)
        plt.savefig('output\\' + name_filter(f'scores increase {data[0][i]["name"]}.png'))
        plt.close()


def name_filter(name: str) -> str:
    forbidden_list = ['\\', '"', '/', '|', '<', '>', '*', ':', '?']
    for sym in forbidden_list:
        name = name.replace(sym, '')
    return name


def data_refresh(data: list[list[dict[str, str | int | float | list[int]]]], param: str = 'w') -> None:
    with open('data.txt', param) as of:
        for d in data:
            of.write(d[0]['date'] + '\n')
            for i in range(10):
                of.write(f'{d[i]} + \n')
            of.write('\n')


def output() -> None:
    if os.path.isdir('output'):
        for file in os.listdir('output'):
            os.remove('output\\' + file)
    else:
        os.mkdir('output')

    data = read_data()

    views(data)
    average_score(data)
    ratings_count(data)
    scores(data)
    scores_in_percent(data)
    views_increase(data)
    average_score_increase(data)
    ratings_count_increase(data)
    scores_increase(data)


if __name__ == '__main__':
    output()
