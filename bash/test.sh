#!/bin/bash

BASE="http://localhost:8000/user"
JSON_DATA="Content-Type: application/json"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OK='\033[0;32mOK\033[0m'
ERROR='\033[0;31mERROR\033[0m'

test_last_command() {
    if [ $? -eq 0 ]; then echo -e $OK;
    else echo -e $ERROR;
    fi;
}

# Inicio de testing. Indicamos que reinicie la base de datos.
printf "Reiniciando base de datos: "
curl -fs -X GET --url "${BASE}/purge" > /dev/null
test_last_command

# Peticion GET para obtener toda la data.
printf "Peticion GET vacia: "
curl -fs -X GET --url "${BASE}/" > /dev/null
test_last_command

# Creamos un usuario.
printf "Creacion de usuario: "
USER_ID=$(curl -fs -X POST -H "${JSON_DATA}" --url "${BASE}/" --data "@${DIR}/data/new-user.json" | jq -r '.ID')
test_last_command

# Intentamos crear un usuario con su correo duplicado. Deberia fallar.
printf "No se permiten duplicados: "
! curl -fs -X POST -H "${JSON_DATA}" --url "${BASE}/" -d @${DIR}/data/duplicate-user.json > /dev/null
test_last_command

# Actualizacion de un usuario.
printf "Actualizacion de usuario: "
curl -fs -X UPDATE -H "${JSON_DATA}" --url "${BASE}/${USER_ID}" -d @${DIR}/data/update-user.json > /dev/null
test_last_command

# Obtenemos el usuario actualizado y nos aseguramos que el nombre sea el correcto
printf "Verificando usuario actualizado: "
NOMBRE=$(curl -fs -X GET --url "${BASE}/${USER_ID}" | jq -r '.Nombre')
test "${NOMBRE}" == "UPDATED"; test_last_command

# Creamos otro usuario adicional
printf "Creando segundo usuario: "
curl -fs -X POST -H "${JSON_DATA}" --url "${BASE}/" --data "@${DIR}/data/2nd-user.json" > /dev/null
test_last_command

# Chequeamos que una fecha invalida no pueda ser utilizada para actualizar
printf "Probando fecha invalida: "
! curl -fs -X UPDATE --url "${BASE}/${USER_ID}" -d "@${DIR}/data/invalid-date.json" > /dev/null
test_last_command

# Lo mismo para un correo invalido
printf "Probando correo invalido: "
! curl -fs -X UPDATE --url "${BASE}/${USER_ID}" -d "@${DIR}/data/invalid-email.json" > /dev/null
test_last_command

# Eliminamos el primer usuario
printf "Eliminando usuario: "
curl -fs -X DELETE --url "${BASE}/${USER_ID}" > /dev/null
test_last_command

# Validamos que intentar obtener el usuario eliminado arroje error
printf "Verificando usuario eliminado: "
! curl -fs -X GET --url "${BASE}/${USER_ID}" > /dev/null
test_last_command

# Finalmente validamos que el segundo usuario aún existe, y es el primero del listado
printf "Verificando datos finales: "
NOMBRE=$(curl -s -X GET --url "${BASE}/" | jq -r '.[0].Nombre')
test "${NOMBRE}" == "Jhon"; test_last_command

echo -e "\n Test finalizados."
