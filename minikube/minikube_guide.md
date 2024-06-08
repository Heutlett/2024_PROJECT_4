# 1. Iniciar Minikube:

`minikube start`

# 2. Para desplegar el Contenedor de SQL Server

## 2.1. Crear un archivo YAML para el despliegue (sqlserver-deployment.yaml)

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sqlserver-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sqlserver
  template:
    metadata:
      labels:
        app: sqlserver
    spec:
      containers:
      - name: sqlserver
        image: mcr.microsoft.com/mssql/server:2019-latest
        ports:
        - containerPort: 1433
        env:
        - name: ACCEPT_EULA
          value: "Y"
        - name: SA_PASSWORD
          value: "Admin1234!"

```

## 2.2. Crear un archivo YAML para el servicio (sqlserver-service.yaml)

```
apiVersion: v1
kind: Service
metadata:
  name: sqlserver-service
spec:
  selector:
    app: sqlserver
  ports:
    - protocol: TCP
      port: 1433
      targetPort: 1433
  type: LoadBalancer

```

# 3. Desplegar en Minikube

```
kubectl apply -f sqlserver-deployment.yaml
kubectl apply -f sqlserver-service.yaml
```

## 3.1. Ver los pods

`kubectl get pods`

# 4. Acceder a la base de datos

`minikube service sqlserver-service --url`

## 4.1. Para acceder a la DB con Azure Data Studio (reemplazar la ip si el comando anterior tira un url diferente)

Server: 192.168.49.2,32423
Authentication type: SQL Login
User name: sa
Password: Admin1234!

# 4.2. Para usar la DB con sqlcmd (reemplazar la ip si el comando anterior tira un url diferente)

sqlcmd -S 192.168.49.2,32423 -U sa -P 'Admin1234!'

# 5. Ejecutar los scripts de creation.sql y population.sql que estan en la carpeta scripts-db