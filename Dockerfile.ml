FROM python:3.9-slim

WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY generator.py .

CMD ["python", "generator.py"]
