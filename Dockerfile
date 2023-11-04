# Usa la imagen oficial de Python como base
FROM python:3.10

# Se establece el directorio de trabajo en el contenedor
WORKDIR /app

# Se copian los archivos a la imagen
COPY dags /app/dags
COPY pokemonAPI.py /app
COPY .env /app

# Se copia el archivo de requisitos
COPY requirements.txt /app

# Instala las dependencias
RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install --no-cache-dir -r requirements.txt

# Da permisos de ejecucion al script pokemonAPI.py
RUN chmod +rx /app/pokemonAPI.py

# Comando para ejecutar el script de DAG
CMD ["python", "dags/dag_poke.py"]