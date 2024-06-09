# Usa una imagen base oficial de Python con Ubuntu slim
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instalar las dependencias del sistema
RUN apt-get update && \
    apt-get install -y curl sudo gnupg apt-transport-https

RUN sudo apt install -y unixodbc unixodbc-dev

# Descargar e instalar la clave GPG de Microsoft
RUN sudo curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

# Agregar el repositorio de Microsoft SQL Server a las fuentes de paquetes
RUN sudo curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Actualizar las fuentes de paquetes e instalar el controlador ODBC de Microsoft SQL Server
RUN apt-get update

RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18 

# Copia los archivos de la aplicación
COPY . .

# Instala las dependencias de la aplicación
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de la aplicación Flask
EXPOSE 5001

# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "crear_usuario.py"]
