# 1. Ejecutar este comando para descargar la key de los credenciales de gcloud para usar el google-cloud-language

`./download_key.sh`

# 2. Exportar la variable de entorno de las credenciales, CAMBIEN el path, debe apuntar al json key.json que acaba de descargar

`export GOOGLE_APPLICATION_CREDENTIALS=/home/heutlett/2024_SOAD_PROJECT_4/microservices/feedback-chatbot/key.json`

# 3. Ejecutar el microservicio

`python3 feedback-chatbot.py`

# 4. Ejecutar request

`http://127.0.0.1:5000/feedback-chatbot?texto=helloworld`