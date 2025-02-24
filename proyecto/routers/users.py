from fastapi import HTTPException, APIRouter, Response, Cookie, Depends
from fastapi.security import HTTPBasicCredentials
from ..database import User
from ..schemas import UserRequestModel, UserResponseModel

router = APIRouter(prefix='/users')


@router.post('', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El username ya se encuentra en uso.')

    hash_password = User.create_password(user.password_hash)

    user = User.create(
        username=user.username,
        email=user.email,
        password_hash=hash_password,
    )

    return user


@router.post('/login', response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(404, 'User not found')

    if user.password_hash != User.create_password(credentials.password):
        raise HTTPException(404, 'Password error')

    response.set_cookie(key='id_user', value=user.id)
    response.set_cookie(key='username', value=user.username)
    response.set_cookie(key='email', value=user.email)

    return user

