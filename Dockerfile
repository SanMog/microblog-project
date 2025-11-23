FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# CMD ["python", "app.py"] # Мы закомментируем это, т.к. будем запускать вручную для разработки