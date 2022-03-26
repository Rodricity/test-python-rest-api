from django.urls import path

from rest_api.models.users.controller import UserController

urlpatterns = [
    # Endpoint especial para testing; Permite reiniciar la base de datos
    path('user/purge', UserController.purge),

    # Manejo para GET/UPDATE/DELETE de un usuario en particular
    path('user/<str:ID>', UserController.handle),

    # Manejo de POST para agregar un usuario
    path('user/', UserController.handle),
]
