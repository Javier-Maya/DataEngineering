# Usa la imagen oficial de Python como base
FROM python:3.10

# Se establece el directorio de trabajo en el contenedor
WORKDIR /app

# Se copian los archivos a la imagen
COPY dags/dag_poke.py /app
COPY requirements.txt /app
COPY pokemonAPI.py /app
COPY .env /app

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el script Python
CMD ["python", "pokemonAPI.py"]

# Comando para ejecutar el script DAG en Apache Airflow
# CMD ["airflow", "dags", "trigger", "dag_poke"]