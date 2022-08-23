from flask import Flask
import sqlite3

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True


def db_connect(query):
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


def get_actors(name_1, name_2):
    """
    Шаг 5. Функция, которая получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех,
    кто играет с ними в паре больше 2 раз.
    """

    query = f"""
                SELECT "cast"
                FROM netflix
                WHERE "cast" LIKE '%{name_1}%'
                AND "cast" LIKE '%{name_2}%'
    """

    response = db_connect(query)
    actors = []
    for cast in response:
        actors.extend(cast[0].split(', '))
    result = []
    for i in actors:
        if i not in [name_1, name_2]:
            if actors.count(i) > 2:
                result.append(i)
    result = set(result)
    return result


def get_type(type_film, release_year, genre):
    """
    Шаг 6. Функция, с помощью которой можно будет передавать тип картины (фильм или сериал),
    год выпуска и ее жанр и получать на выходе список названий картин с их описаниями в JSON.
    """

    query = f"""
                SELECT title, description, "type"
                FROM netflix
                WHERE "type" = '{type_film}'
                AND release_year = {release_year}
                AND "listed_in" LIKE '%{genre}%'
    """

    response = db_connect(query)
    response_json = []
    for film in response:
        response_json.append({
            'title': film[0],
            'description': film[1].strip(),
            'type': film[2],
        })

    return response_json


print(get_type(type_film='Movie', release_year=2016, genre='Dramas'))
# print(get_actors(name_1='Rose McIver', name_2='Ben Lamb'))
