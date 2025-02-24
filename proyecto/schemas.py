from typing import Any, Optional
from pydantic import BaseModel, field_validator, ValidationError, validator
from pydantic.v1.utils import GetterDict
from peewee import ModelSelect
from datetime import datetime


#  Convertir objeto tipo Model (peewee) a diccionario
class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        # Obtener cada uno de los atributos de objeto Model y comparar con ResponseModel
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res

# ------------------ Users ------------------


class ResponseModel(BaseModel):
    #  Sirve para responder con objeto tipo JSON. Convertir modelos de peewee a modelos de pydantic
    class Config:
        from_attributes = True


class UserRequestModel(BaseModel):
    username: str
    email: str
    password_hash: str

    @field_validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('La longitud debe de encontrarse entre 3 y 50 caracteres.')

        return username


class UserResponseModel(ResponseModel):
    username: str
    email: str


class UserRequestPutModel(BaseModel):
    username: str
    email: str


class UserRequestDeleteModel(BaseModel):
    id_user: int
    username: str
    email: str
    password_hash: str


# ------------------ Tasks ------------------


class TaskRequestModel(BaseModel):
    id_user: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    @field_validator('title')
    def title_validator(cls, title):
        if len(title) < 3 or len(title) > 100:
            raise ValueError('La longitud del título debe estar entre 3 y 100 caracteres.')
        return title


class TaskResponseModel(ResponseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    id_user: UserResponseModel


class TaskRequestPutModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator('title')
    def title_validator(cls, title):
        if title and (len(title) < 3 or len(title) > 100):
            raise ValueError('La longitud del título debe estar entre 3 y 100 caracteres.')
        return title


class TaskRequestDeleteModel(BaseModel):
    id_task: int
    user_id: Optional[int] = None

