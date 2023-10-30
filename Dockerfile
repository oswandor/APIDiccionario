# Utilizar una imagen base de Python 3.8
FROM python:3.11.6-bullseye

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar los archivos de la aplicación en el contenedor
COPY . /app

# Instalar las dependencias de la aplicación
RUN pip install -r requirements.txt

# Exponer el puerto en el que se ejecutará la aplicación Flask
EXPOSE 5000


ENV MONGO_URI="mongodb+srv://oswandor26:u3w6dhSXLjZ3iN0g@cluster0.mmmsz3e.mongodb.net/?retryWrites=true&w=majority"
# Comando para ejecutar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0"]
