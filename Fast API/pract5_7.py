"""
#### Задание №7
- Создать RESTful API для управления списком задач. Приложение должно
использовать FastAPI и поддерживать следующие функции:
○ Получение списка всех задач.
○ Получение информации о задаче по её ID.
○ Добавление новой задачи.
○ Обновление информации о задаче по её ID.
○ Удаление задачи по её ID.
- Каждая задача должна содержать следующие поля: ID (целое число),
Название (строка), Описание (строка), Статус (строка): "todo", "in progress",
"done".
- Создайте модуль приложения и настройте сервер и маршрутизацию.
- Создайте класс Task с полями id, title, description и status.
- Создайте список tasks для хранения задач.
- Создайте функцию get_tasks для получения списка всех задач (метод GET).
- Создайте функцию get_task для получения информации о задаче по её ID
(метод GET).
- Создайте функцию create_task для добавления новой задачи (метод POST).
- Создайте функцию update_task для обновления информации о задаче по её ID
(метод PUT).
- Создайте функцию delete_task для удаления задачи по её ID (метод DELETE).
"""
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from starlette.responses import JSONResponse


app = FastAPI()


TASKS: list = []


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str


@app.get("/get_tasks/")
async def get_tasks():
    #return {"ALL_TASKS": TASKS}
    all_task_dicts = [task.dict() for task in TASKS]
    return JSONResponse(content=all_task_dicts, status_code=200)


@app.get("/get_task/{id_task}")
async def get_task(id_task: int):

    answer: list = []

    for task_from_list in TASKS:
        if task_from_list.id == id_task:
            answer.append(task_from_list)

    if answer:
        return {"task": answer}
    else:
        return {"error": "Task with this id is not in the database."}


@app.post("/create_task/")
async def create_task(task: Task):

    for task_from_list in TASKS:
        if task_from_list.id == task.id:
            return {"error": "Task with this id already exists"}

    TASKS.append(task)
    return {"add_task": task}





@app.put("/update_task/")
async def update_task(task: Task):

    for task_from_list in TASKS:

        if task_from_list.id == task.id:
            task_from_list.title = task.title
            task_from_list.description = task.description
            task_from_list.status = task.status

            return {"update_task": task}

    return {"error": "Task not found"}





@app.delete("/delete_task/{id_task}")
async def delete_task(id_task: int):

    count: int = 0

    for task_from_list in TASKS:
        if task_from_list.id == id_task:
            TASKS.pop(count)
            return {"delete_task": task_from_list}
        count += 1
    return {"error": "Task not found"}