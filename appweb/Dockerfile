# Usar una imagen base ligera de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos y el código fuente
COPY dependencies.txt dependencies.txt
RUN pip install --no-cache-dir -r dependencies.txt

COPY . .

# Exponer el puerto que usará la aplicación
EXPOSE 5000

# Establecer credenciales dummy para AWS
ENV AWS_ACCESS_KEY_ID=test
ENV AWS_SECRET_ACCESS_KEY=test
ENV AWS_DEFAULT_REGION=us-east-1

# Comando para iniciar la aplicación
CMD ["python", "app.py"]