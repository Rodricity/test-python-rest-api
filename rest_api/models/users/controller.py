import json
from django.http import HttpResponse, HttpResponseBadRequest,  HttpResponseNotFound
from email_validator import EmailSyntaxError
from jsonpickle import encode
from rest_api.models.users.model import USERS_DB, User
from rest_api.exceptions import DuplicateUserError, InvalidDateException, UserNotFound


class UserController():
    @staticmethod
    def handle(request, ID=None):
        if request.method == "GET":
            return UserController.get(request, ID)

        if request.method == "POST":
            return UserController.post(request)

        if(request.method == "UPDATE"):
            return UserController.update(request, ID)

        if(request.method == "DELETE"):
            return UserController.delete(request, ID)

        return HttpResponseBadRequest()

    # Método para crear nuevos usuarios
    @staticmethod
    def post(request):

        try:
            data = json.loads(request.body)
            newUser = User(data["Nombre"], data["Apellido"], data["Email"], data["FechaNacimiento"])
            newUser.save()
            return HttpResponse(newUser)
        except (DuplicateUserError, json.JSONDecodeError):
            return HttpResponseBadRequest()

    # GET para obtener un usuario en particular o bien todos los usuarios.
    @staticmethod
    def get(request, ID):

        # Si no me entregan un ID como string; Asumimos que pidieron todo.
        if isinstance(ID, str) == False:
            return HttpResponse(encode(User.getAll(), unpicklable=False))

        # De lo contrario buscamos un usuario y controlamos si es que no existiera.
        else:
            try:
                return HttpResponse(User.get(ID))
            except UserNotFound:
                return HttpResponseNotFound()

    # PUT para actualizar la data de un usuario en particular.
    @staticmethod
    def update(request, ID):

        if isinstance(ID, str) == False:
            return HttpResponseBadRequest()

        try:
            user = User.get(ID)
            data = json.loads(request.body)
            user.update(data["Nombre"], data["Apellido"], data["Email"], data["FechaNacimiento"])
            user.save()

            return HttpResponse(user)
        except (UserNotFound):
            return HttpResponseNotFound()
        except (InvalidDateException, EmailSyntaxError, json.JSONDecodeError) as e:
            return HttpResponseBadRequest()

    # DELETE para eliminar algún usuario
    @staticmethod
    def delete(request, ID):
        if isinstance(ID, str) == False:
            return HttpResponseBadRequest()

        try:
            user = User.get(ID)
            user.delete()
            return HttpResponse()
        except:
            return HttpResponseNotFound()

    @staticmethod
    def purge(request):
        USERS_DB.clear()
        return HttpResponse()
