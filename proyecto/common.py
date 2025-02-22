from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from proyecto.database import User
import jwt

SECRET_KEY = 'EjemploDeSecreto'
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/auth')


def create_access_token(user, days=7):
    data = {
        'id_user': user.id,
        'username': user.username,
        'exp': datetime.now() + timedelta(days=days)
    }

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ha expirado")
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no válido")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error de autenticación")


def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    data = decode_access_token(token)
    #  Obtener usuario autenticado
    if data:
        return User.select().where(User.id == data['id_user']).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access Token no valido',
            headers={'WWW-Authenticate': 'Bearer'}
        )
