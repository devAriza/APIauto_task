import hashlib
from peewee import *
from datetime import datetime

nameBD = 'auto_task'
usuario = 'root'
host = 'localhost'
puerto = 3306

database = MySQLDatabase(nameBD, user=usuario, password='Mysql12345', host=host, port=puerto)


class User(Model):

    #  id_user = AutoField()
    username = CharField(max_length=50, unique=True)
    email = CharField(max_length=50)
    password_hash = CharField(max_length=50)

    def __str__(self):
        return {'id': self.id, 'username': self.username}

    class Meta:
        database = database
        table_name = 'users'

    @classmethod
    def authenticate(cls, username, password_hash):
        user = cls.select().where(User.username == username).first()
        if user and user.password_hash == cls.create_password(password_hash):
            return user

    # Encriptar contraseña
    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))

        return h.hexdigest()  # retornar hexadecimal


class Task(Model):
    title = CharField(max_length=50)
    description = TextField(null=True)
    completed = BooleanField(default=False)
    id_user = ForeignKeyField(User, backref='tasks', column_name="id_user")

    def __str__(self):
        return f'Tarea: {self.title} - Usuario: {self.id_user}'

    class Meta:
        database = database
        table_name = 'tasks'
