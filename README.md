# 2024_PROJECT_4

## INPUTS METODOS 

Algunos metodos requieren como input un body en formato json, mientras que otros metodos requieren como input parametros en la url.

### LOGIN 

crear-usuario (POST)

```
{
    "data":{
        "username": "gato",
        "password": "soa",
        "first_name": "Jimena",
        "last_name1": "Leon",
        "last_name2": "Huertas",
        "security_question": "Color favorito?",
        "security_answer": "Verde" 
    }
}

obtener-usuario (GET): devuelve un token que contiene el username y contrasena cifrados de un usuario.

```
Con params:
http://ip/obtener-usuario?username=client1&password=client1
```
```

cambiar-contrasena (PUT)
```
{
    "data":{
        "method": "cambiar-contrasena",
        "username": "client1",
        "new_password": "client1",
        "security_answer":"Blue"
    }
}
```


### RESERVA: algunos de estos metodos requieren token, por lo cual se debe usar primero el metodo obtener-usuario para conseguir dicho token. Recuerde que el token expira cada cierto tiempo

crear-reserva (POST)

```
{
    "data":{
        "method":"crear-reserva",
        "token":"hay que obtener un token con el metodo de obtener-usuario",
        "restaurant_id":"2",
        "number_of_people": "2",
        "reservation_date": "2024-10-03",
        "start_time":"12:00:00",
        "selected_tables":[
            1
        ]
    }
}
```

### RECOMENDACION

### HORARIO