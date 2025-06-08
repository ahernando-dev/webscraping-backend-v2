FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

# Crea el directorio de trabajo
WORKDIR /app

# Copia los archivos del backend
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de Uvicorn
EXPOSE 10000

# Comando para arrancar el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]