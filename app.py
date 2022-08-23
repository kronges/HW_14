from flask import Flask, jsonify
import sqlite3
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def main():
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

    @app.route('/movie/<title>')
    def search_by_title(title):
        """ Шаг 1. Поиск по названию самого свежего """
        logging.info(f'Поисковая фраза: {title}')

        query = f"""
                SELECT title, country, release_year, listed_in AS genre, description
                FROM netflix
                WHERE title = '{title}'
                ORDER BY release_year DESC
                LIMIT 1
        """

        response = db_connect(query)[0]
        response_json = {
            "title": response[0],
            "country": response[1],
            "release_year": response[2],
            "genre": response[3],
            "description": response[4],
        }
        logging.info(f'search_by_title вернул: {response_json}')

        return jsonify(response_json)

    @app.route('/movie/<start>/to/<end>')
    def search_by_years(start, end):
        """ Шаг 2. Поиск по диапазону лет выпуска(от start до end)  """

        logging.info(f'Год поиска от {start} до {end}')

        query = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN {start} AND {end}
                    ORDER BY release_year
                    LIMIT 100
            """

        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                "title": film[0],
                "release_year": film[1],
            })

        return jsonify(response_json)

    @app.route('/rating/<group>')
    def search_by_rating(group):
        """ Шаг 3. Поиск по рейтингу  """

        groups = {
            'children': ['G'],
            'family': ['G', 'PG', 'PG-13'],
            'adult': ['R', 'NC-17']
        }
        if group in groups:
            rating = '\", \"'.join(groups[group])
            rating = f'\"{rating}\"'
        else:
            return 'Группа введена не правильно, проверьте написание группы: children, family, adult'

        logging.info(f'Поиск по группе {groups}')

        query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ({rating})
            """
        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                "title": film[0].strip(),
                "rating": film[1],
                "description": film[2].strip(),
            })

        return jsonify(response_json)

    @app.route('/genre/<genre>')
    def search_by_genre(genre):
        """ Шаг 4. Функция, которая получает название жанра в качестве аргумента
        и возвращает 10 самых свежих фильмов в формате json.
        """

        logging.info(f'Выбранный жанр {genre}')

        query = f"""
                    SELECT title, description, listed_in, release_year
                    FROM netflix
                    WHERE "listed_in" LIKE '%{genre}%'
                    ORDER BY release_year DESC 
                    LIMIT 10
            """

        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                "title": film[0],
                "description": film[1],
                "listed_in": film[2],
                "release_year": film[3],
            })

        return jsonify(response_json)


    app.run(debug=True)


if __name__ == '__main__':
    main()
