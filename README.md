# 2024_PROJECT_4

## INPUTS METODOS 

Algunos metodos requieren como input un body en formato json, mientras que otros metodos requieren como input parametros en la url.

### LOGIN 

#### crear-usuario (POST)

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
```

#### obtener-usuario (GET): devuelve un token que contiene el username y contrasena cifrados de un usuario

```
http://ip/obtener-usuario?username=client1&password=client1
```

#### verificar-usuario (GET): devuelve un usuario segun el token dado

```
http://ip/verificar-usuario?token=qweqweqwe
```

#### cambiar-contrasena (PUT)

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

#### crear-reserva (POST)

```
{
    "data":{
        "method":"crear-reserva",
        "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNsaWVudDEiLCJwYXNzd29yZCI6ImNsaWVudDEiLCJleHAiOjE3MTgwOTMzOTR9.T4wmU4IEz0fjm_cc3oPP-RoQLJ731q4lVvjH6JbyffQ",
        "restaurant_id":1,
        "number_of_people": 2,
        "reservation_date": "2024-10-04",
        "start_time":"12:00:00",
        "selected_tables":[
            1
        ]
    }
}
```

#### editar-reserva (PUT): solo se pueden editar reservas futuras

```
{
    "data":{
        "method":"crear-reserva",
        "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNsaWVudDEiLCJwYXNzd29yZCI6ImNsaWVudDEiLCJleHAiOjE3MTgwOTMzOTR9.T4wmU4IEz0fjm_cc3oPP-RoQLJ731q4lVvjH6JbyffQ",
        "reservation_id":3
        "restaurant_id":1,
        "number_of_people": 2,
        "reservation_date": "2024-10-04",
        "start_time":"12:00:00",
        "selected_tables":[
            1
        ]
    }
}
```
#### obtener-calendario (GET): pendiente

PENDIENTE DE IMPLEMENTAR

```
URL con params
```

#### obtener-reserva-puntual (GET)

```
http://ip/obtener-reserva/?reservation_id=3
```

#### obtener-reservas-futuras (GET): obtiene las reservas futuras de 1 usuario

```
http://ip/obtener-reserva/?time=futuras&token=conseguirtoken
```

#### obtener-reservas-pasadas (GET): obtiene las reservas pasadas de 1 usuario

```
http://ip/obtener-reserva/?time=futuras&token=conseguirtoken
```

#### obtener-reservas-todas (GET): obtiene todas las reservas FUTURAS de TODOS los usuarios

```
http://ip/obtener-reserva/?time=all
```

#### eliminar-reserva (DELETE)

```
{
    "data":{
        "method": "eliminar-reserva",
        "token":"eeeeeeeeeee",
        "reservation_date":"2024-10-04",
        "reservation_id":3
        "restaurant_id":1 
        "start_time":"12:00:00" 
    }
}        
```

### RECOMENDACION

#### obtener-menu (GET)

```
http://ip/obtener-menu
```

#### obtener-recomendacion (GET): se usan los IDs de los platillos

1 platillo input, 2 platillos de recomendacion:

```
http://ip/obtener-recomendacion?dish1=1
```

2 platillos input, 1 platillo recomendacion:

```
http://ip/obtener-recomendacion?dish1=1&dish2=41
```

### HORARIO

#### ampliar-disponibilidad (PUT): amplia el horario de apertura y cierre de un restaurante dado

PENDIENTE DE IMPLEMENTAR

```
{
    {
        "data": {
            "method":"ampliar-disponibilidad",
            "restaurant_id": 2,
            "hora_apertura": "07:00:00",
            "hora_cierre": "23:00:00"
        }
    }
}
```

### FEEDBACK

#### feedback-chatbot (GET): obtiene 

```
http://ip/feedback-chatbot?texto=Estoyalegre
```