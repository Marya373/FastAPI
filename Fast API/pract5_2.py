"""
#### Задание №2
- Создать API для получения списка фильмов по жанру. Приложение должно
иметь возможность получать список фильмов по заданному жанру.
- Создайте модуль приложения и настройте сервер и маршрутизацию.
- Создайте класс Movie с полями id, title, description и genre.
- Создайте список movies для хранения фильмов.
- Создайте маршрут для получения списка фильмов по жанру (метод GET).
- Реализуйте валидацию данных запроса и ответа.
"""
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


MOVIES: list = []


class Movie(BaseModel):
    id: int
    title: str
    description: str
    genre: str


@app.post("/add_movie/")
async def add_movie(movie: Movie):

    for movie_from_list in MOVIES:
        if movie_from_list.id == movie.id:
            return {"error": "Movie with this id already exists"}

    MOVIES.append(movie)
    return {"add_movie": movie}


@app.get("/get_movies/{genre}")
async def get_movies(genre: str):

    answer: list = []

    for movie_from_list in MOVIES:
        if movie_from_list.genre == genre:
            answer.append(movie_from_list)

    if answer:
        return {"genre": answer}
    else:
        return {"error": "There are no films in this genre in the database"}
