from fastapi import HTTPException, APIRouter, Depends
from starlette import status

from ..database import User, Task
from ..schemas import TaskRequestModel, TaskResponseModel, TaskRequestPutModel, TaskRequestDeleteModel
from ..common import get_current_user, oauth2_schema


router = APIRouter(prefix='/tasks')



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



