"""
#### Задание №1
- Создать API для управления списком задач. Приложение должно иметь
возможность создавать, обновлять, удалять и получать список задач.
- Создайте модуль приложения и настройте сервер и маршрутизацию.
- Создайте класс Task с полями id, title, description и status.
- Создайте список tasks для хранения задач.
- Создайте маршрут для получения списка задач (метод GET).
- Создайте маршрут для создания новой задачи (метод POST).
- Создайте маршрут для обновления задачи (метод PUT).
- Создайте маршрут для удаления задачи (метод DELETE).
- Реализуйте валидацию данных запроса и ответа.
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
    status: bool


@app.get("/get_all_task/")
async def get_all_task():
    #return {"ALL_TASKS": TASKS}
    all_task_dicts = [task.dict() for task in TASKS]
    return JSONResponse(content=all_task_dicts, status_code=200)


@app.post("/create_task/")
async def create_task(task: Task):

    for task_from_list in TASKS:
        if task_from_list.id == task.id:
            return {"error": "Task with this id already exists"}

    TASKS.append(task)
    return {"add_task": task}


#@app.put("/change_task/id_task/")
#async def change_task(task: Task, id_task: int):
#
#    for task_from_list in TASKS:
#
#        if task_from_list.id == id_task:
#            task_from_list.title = task.title
#            task_from_list.description = task.description
#            task_from_list.status = task.status
#            return {"change_task": task}
#
#    return {"error": "Task not found"}


@app.put("/change_task/")
async def change_task(task: Task):

    for task_from_list in TASKS:

        if task_from_list.id == task.id:
            task_from_list.title = task.title
            task_from_list.description = task.description
            task_from_list.status = task.status

            return {"change_task": task}

    return {"error": "Task not found"}


#@app.delete("/delete_task/")
#async def delete_task(task: Task):
#
#    sequence_number: int = -1
#
#    for number_task in range(len(TASKS)):
#
#        if TASKS[number_task].id == task.id:
#            sequence_number = number_task
#
#    if sequence_number < 0:
#        return {"error": "Task not found"}
#    else:
#        TASKS.pop(sequence_number)
#        return {"delete_task": task}


@app.delete("/delete_task/{id_task}")
async def delete_task(id_task: int):

    count: int = 0

    for task_from_list in TASKS:
        if task_from_list.id == id_task:
            TASKS.pop(count)
            return {"delete_task": task_from_list}
        count += 1
    return {"error": "Task not found"}