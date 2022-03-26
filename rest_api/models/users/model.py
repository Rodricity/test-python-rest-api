from __future__ import annotations
from datetime import date
import datetime
import re
from email_validator import validate_email
import json
import uuid
from rest_api.exceptions import DuplicateUserError, InvalidDateException, UserNotFound

# Almacenamiento en memoria de los 'usuarios'
USERS_DB = []

""" Modelo de usuario según especificaciones """


class User:
    ID: str = None
    Nombre: str
    Apellido: str
    Email: str
    FechaNacimiento: date

    def __init__(self, nombre, apellido, email, fechaNacimiento):

        self.Nombre = nombre
        self.Apellido = apellido
        self.Email = self.__validarEmail(email)
        self.FechaNacimiento = self.__validarFechaNacimiento(fechaNacimiento)

    # Obtiene un usuario a partir de su ID.
    @staticmethod
    def get(id) -> User:
        for user in USERS_DB:
            if user.ID == id:
                return user

        raise UserNotFound("User not found: " + id)

    # Retorna todos los usuarios de la base de datos
    @staticmethod
    def getAll():
        return USERS_DB

    # Funcion para actualizar un usuario. Valida que el email no se pueda duplicar.
    def update(self, nombre, apellido, email, fechaNacimiento):

        validEmail = self.__validarEmail(email)
        validDate = self.__validarFechaNacimiento(fechaNacimiento)

        self.Email = validEmail
        self.Nombre = nombre
        self.Apellido = apellido
        self.FechaNacimiento = validDate

    # Guarda el usuario en la 'base de datos'
    def save(self):
        # Si este usuario ya tiene ID; Entonces ya está dentro de la 'base de datos'
        if(self.ID != None):
            return

        # Caso contrario, generamos un UUID y guardamos.
        self.ID = uuid.uuid4().__str__()
        USERS_DB.append(self)

    # Borra este usuario en particular
    def delete(self):
        USERS_DB.remove(self)

    def __validarEmail(self, nuevoMail):
        # Nos aseguramos que el email sea valido, de lo contrario levanta una excepcion
        email_validation = validate_email(nuevoMail)
        email = email_validation["email"]

        # Verificamos que ningun otro usuario tiene este correo.
        for user in USERS_DB:
            if(self != user and email == user.Email):
                raise DuplicateUserError("Duplicate email: " + email)

        return email

    # Método para validar que la fecha de nacimiento tenga el formato correcto.
    def __validarFechaNacimiento(self, nuevaFecha):
        f = re.match("(\d{4})-(\d{2})-(\d{2})", nuevaFecha)
        if bool(f) == False:
            raise InvalidDateException("Invalid date input: " + nuevaFecha)

        return datetime.datetime(int(f[1]), int(f[2]), int(f[3]))

    # Helper para poder imprimir un User en formato JSON

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, default=str)
