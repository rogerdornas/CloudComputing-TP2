# Usa uma imagem leve do Python
FROM python:3.9-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do gerador
COPY generator.py .

# Define o comando padrão para rodar quando o container iniciar
# Ele vai executar o script e depois encerrar (o que é correto para um Job de ML)
CMD ["python", "generator.py"]
