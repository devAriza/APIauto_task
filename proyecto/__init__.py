from fastapi import FastAPI, APIRouter, Depends, HTTPException,status
from .database import User, Task
from .database import database as connection
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from .common import create_access_token

from .routers import user_router
from .routers import task_router


app = FastAPI(title='CRUD Tasks',
              description='Assesment of CRUD Tasks',
              version='1'
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Permite solicitudes desde tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

api_v1 = APIRouter(prefix='/api')

api_v1.include_router(user_router)
api_v1.include_router(task_router)

@app.on_event('startup')
async def startup_event():
    if connection.is_closed():
        connection.connect()

    #  Crear de tablas. En caso de existir no pasa nada
    connection.create_tables([User, Task])

@api_v1.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):

    user = User.authenticate(data.username, data.password)

    if user:
        return{
            'access_token': create_access_token(user),
            'token_type': 'Bearer'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Username o password incorrectos',
            headers={'WWW-Authenticate': 'Bearer'}
        )


app.include_router(api_v1)

@app.on_event('shutdown')
def shutdown_event():
    if not connection.is_closed():
        connection.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}
