# Etapa 1: Imagem base
FROM python:3.12-slim

# Etapa 2: Diretório de trabalho dentro do container
WORKDIR /app

# Etapa 3: Copia os arquivos de dependência
COPY requirements.txt .

# Etapa 4: Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copia o restante dos arquivos do projeto
COPY . .

# Etapa 6: Expõe a porta usada pelo Uvicorn
EXPOSE 8000

# Etapa 7: Comando para iniciar o app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
