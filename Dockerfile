# Imagem base com Python em versão leve.
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Copia o arquivo de dependências primeiro para aproveitar cache do Docker.
COPY requirements.txt .

# Instala as dependências do projeto.
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para dentro do container.
COPY . .

# Expõe a porta padrão usada pelo Uvicorn/FastAPI.
EXPOSE 8000

# Comando para iniciar a API.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]