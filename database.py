import psycopg2
from functools import wraps
from typing import Callable


def connection(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: any):
        con = psycopg2.connect(database="postgres", user="postgres", password="", host="127.0.0.1", port="5432")
        cur = con.cursor()
        output = func(cur, *args)
        con.commit()
        con.close()
        return output
    return wrapper


@connection
def create_table(cur: psycopg2) -> None:
    cur.execute("""CREATE TABLE STATISTIC
    (DATE TEXT NOT NULL,
    NAME TEXT NOT NULL,
    AVERAGE_SCORE REAL NOT NULL,
    RATINGS_COUNT INT NOT NULL,
    VIEWS_COUNT INT NOT NULL,
    RATINGS TEXT NOT NULL);""")


@connection
def drop_table(cur: psycopg2) -> None:
    cur.execute("""DROP TABLE STATISTIC""")


@connection
def clear_table(cur: psycopg2) -> None:
    cur.execute("""DELETE FROM STATISTIC""")


@connection
def write_data(cur: psycopg2, date: str, data: list[dict[str, str | int | float | list[int]]]) -> None:
    for d in data:
        cur.execute("""INSERT INTO STATISTIC (DATE, NAME, AVERAGE_SCORE, RATINGS_COUNT, VIEWS_COUNT, RATINGS) 
        VALUES (%s, %s, %s, %s, %s, %s)""", (date, d['name'], d['average_score'], d['ratings_count'],
                                             d['views_count'], d['ratings']))


@connection
def read_data(cur: psycopg2) -> list[list[dict[str, str | int | float | list[int]]]]:
    cur.execute("""SELECT DATE, NAME, AVERAGE_SCORE, RATINGS_COUNT, VIEWS_COUNT, RATINGS FROM STATISTIC""")
    rows = cur.fetchall()
    data_list, all_data, i = [], [], 0

    for row in rows:
        data = {'date': row[0], 'name': row[1], 'average_score': row[2], 'ratings_count': row[3],
                'views_count': row[4], 'ratings': list(map(int, row[5][1:-1].split(',')))}
        data_list.append(data)
        i += 1
        if i == 10:
            all_data.append(data_list)
            data_list = []
            i = 0

    return all_data
