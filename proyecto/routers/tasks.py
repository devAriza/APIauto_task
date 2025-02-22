from fastapi import HTTPException, APIRouter, Depends
from starlette import status

from ..database import User, Task
from ..schemas import TaskRequestModel, TaskResponseModel, TaskRequestPutModel, TaskRequestDeleteModel
from ..common import get_current_user, oauth2_schema
from typing import List


router = APIRouter(prefix='/tasks')


@router.get('/get_task/{task_id}', response_model=TaskResponseModel)
async def get_tasks(task_id: int, user: User = Depends(get_current_user)):

    task = Task.select().where(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')

    if task.id_user.id != user.id:
        raise HTTPException(status_code=401, detail='No eres propietario')

    return task


@router.get('/get_tasks/', response_model=List[TaskResponseModel])
async def get_tasks(user: User = Depends(get_current_user)):

    return [task for task in user.tasks]

@router.post('/create_task', response_model=TaskResponseModel)
async def create_task(user_tasks: TaskRequestModel, user: User = Depends(get_current_user)):
    """
    Creates new review tasks
    :param user_tasks: Modelo de la tarea
    :param user: Obtener id identificado
    :return: Dict con tarea creada
    """

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if User.select().where(User.id == user_tasks.id_user).first() is None:
        raise HTTPException(status_code=404, detail='User not found')

    user_tasks = Task.create(
        title=user_tasks.title,
        description=user_tasks.description,
        completed=user_tasks.completed,
        id_user=user,
    )
    return user_tasks


@router.put('/update_task/{task_id}', response_model=TaskResponseModel)
async def update_task(task_id: int, task_request: TaskRequestPutModel, user: User = Depends(get_current_user)):

    task = Task.select().where(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')

    if task.id_user.id != user.id:
        raise HTTPException(status_code=401, detail='No eres propietario')

    task.title = task_request.title
    task.description = task_request.description
    task.completed = task_request.completed

    task.save()
    return task

@router.delete('/delete_task/{task_id}', response_model=TaskResponseModel)
async def delete_task(task_id: int, user: User = Depends(get_current_user)):

    task = Task.select().where(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')

    if task.id_user.id != user.id:
        raise HTTPException(status_code=401, detail='No eres propietario')

    task.delete_instance()
    return task

