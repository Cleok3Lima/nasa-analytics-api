FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install fastapi[all] uvicorn psycopg2 sqlalchemy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
