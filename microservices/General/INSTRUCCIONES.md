## 0. Explicacion y requisitos

Todos los microservicios van a estar en el mismo POD (cluster o grupo de contenedores). Cada microservicio es un contenedor de Docker, cuya imagen estara guardada en Dockerhub.

La base de datos va a estar en un POD distinto para no tener que borrarla y crearla cada vez que agregamos un microservicio.

### Requisitos

Tener instalado:
1. Docker Desktop (y dejarlo abierto siempre. No lo cierre)
2. Minikube
3. kubectl
4. Python 3.10 como minimo
5. Usar Ubuntu por fis (se puede en Windows pero es feo)

## 1. Desplegar la Base de Datos en Minikube

Para esto vea el "minikube_guide.md" de la carpeta minikube. Use Azure Data Studio para correr los scrips de creacion y populacion.

## 2. Desarrollar el microservicio en Python Flask

### 2.1 Vaya a la carpeta microservices

### 2.2. Use las librerias de Flask, request y Pyodbc como minimo

Instale todo lo anterior con estos comandos:

```
pip install pyodbc
pip install Flask
```

Instalar el driver para pyodbc con estos comandos:

```
curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

sudo apt-get update

sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

### 2.3 Cree un archivo requirements.txt y escriba todas las librerias de Python necesarias

Para esto primero verifique las versiones que usted tenga instaladas en su PC. Puede hacer este comando para eso:

```
pip show <libreria>
```
En el requirements.txt ponga libreria==version para todas las librerias

### 2.4 Probar el requirements.txt

Haga este comando:

```
 pip install -r requirements.txt
 ```

### 2.5 Termine de programar el microservicio y pruebelo localmente 

Use de guia los microservicios que ya sirven. Para el codigo, copielo del repo sel proyecto 3 y le quita las cosas de Cloud Functions, las librerias viejas de base de datos y lo de pub-sub si tuviera. 

Para probarlo, corralo normalmente:

```
python3 <archivo>.py 
```

Use Postman para probar. Recuerde que estos microservicios al final de cuentas simplemente son APIs REST chiquititos con HTTP.

## 3. Desplegar microservicio en Minikube

### 3.1 Haga un Dockerfile para el microservicio. 

Copie alguno de los Dockerfile de algun microservicio que ya sirva. Esto es para que Minikube pueda instalar el driver de Pyodbc que usted instaló en el paso 1.2.

En el Dockerfile solo cambiele estas lineas del final del archivo:


```
# Exponer el puerto de la aplicación Flask
EXPOSE <numero> # El puerto va a ser siempre 500X. 
```

Para saber cual numero poner, revise el yaml y se dara cuenta de cual fue el ultimo numero. El siguiente a ese sera el que debe poner. Importante: Los puertos de los archivos yaml deben coincidir con los de los archivos Dockerfile.

Finalmente escriba el nombre del microservicio en esta linea de codigo:

```
# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "<microservicio>.py"]
```

### 3.2 Ir al archivo multiconontainer-deployment.yaml y agregar esta linea:

Cambiele el nombre a las cosas que tengan <>

```
- name: <microservicio>
        image: <your-dockerhub-user>/<microservicio>:latest
        ports:
        - containerPort: <revisar el que siga en el archivo>

```

### 3.3 Ir al archivo multicontainer-service.yaml y agregar esta linea:

Cambiele el nombre a las cosas que tengan <>. Si tiene duda con cuales numeros poner siga el "patron" de los archivos yaml de los otros microservicios

```
- name: <microservicio>
      protocol: TCP
      port: <numero>
      targetPort: <container-port-number>  # Puerto del contenedor <microservicio>
      nodePort: <node-port-number>  # Puerto asignado en los nodos del clúster
```

### 3.4 Subir imagen de Docker a Dockerhub

Ingrese a Dockerhub con la misma cuenta de Docker: https://hub.docker.com/

Cree un archivo run_docker_image.sh (para Linux) y escriba estas lineas:

```
eval $(minikube docker-env) # Si esta en Windows este comando es distinto
docker build -t <microservicio>:latest .
docker tag <microservicio>:latest <dockerhub-user>/<microservicio>:latest
docker login
docker push <dockerhub-user>/<microservicio>:latest
```

Esto es para subir una imagen a su cuenta de Dockerhub y que Minikube pueda acceder a esa imagen. Sin esto no funciona.

Dele permisos al archivo con este comando:

```
chmod 777 "run_docker_image.sh"
```

### 3.5 Modificar el run.sh general

Una vez que creó el run_docker_image.sh, vayase al archivo run.sh que esta dentro de la carpeta microservices (ojo que ese archivo deberia estar fuera de las subcarpetas especificas de cada microservicio)

Agregue esta linea:

```
cd <carpeta_microservicio>/ && ./run_docker_image.sh && cd ../
```

Y agregue estas dos lineas:

```
kubectl delete deployment <microservicio>
kubectl delete service <microservicio>-service
```

### 3.6 Correr el run.sh

Dele permisos al run.sh con el comando:

```
chmod 777 "run.sh"
```

Ejecutelo con este otro comando:

```
./run.sh
```

El archivo run.sh corre por debajo su archivo run_docker_image.sh y hace configuraciones de Minikube para desplegar el microservicio.

Listo!

### 3.7 Ejecutar lo siguiente y observar el orden de las url, usar las que aparecen con 127.0.0.1:
![alt text](image.png)