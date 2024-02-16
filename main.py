import time
from database import write_data
from parsing import parsing


def timer() -> str:
    system_time = str(time.strftime("%H:%M:%S %d.%m.%Y", time.localtime()))
    return system_time


def write_log(exit_code: int, t: str) -> None:
    exit_list = {200: 'Успешно', -1: 'Ошибка соединения', 403: 'Отказ в доступе', 404: 'Страница не найдена',
                 503: 'Временно недоступен', 999: 'Неизвестная ошибка'}

    with open('log.txt', 'a') as output_file:
        output_file.write(t + '\n')
        output_file.write(f'Задача завершена с кодом {exit_code} '
                          f'({exit_list[exit_code] if exit_code in exit_list else exit_list[999]})\n\n')


def main() -> None:
    data, exit_code = parsing()
    t = timer()
    write_log(exit_code, t)
    if exit_code == 200:
        write_data(t, data)


if __name__ == '__main__':
    main()
