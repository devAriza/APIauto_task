from fastapi import FastAPI, APIRouter, Depends, HTTPException,status

from .database import User, Task
from .database import database as connection
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .common import create_access_token

from .routers import user_router
from .routers import task_router


app = FastAPI(title='CRUD Tasks',
              description='Assesment of CRUD Tasks',
              version='1'
              )

app.mount("/", StaticFiles(directory="static", html=True), name="static")

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
    return RedirectResponse(url='/static/login.html')
