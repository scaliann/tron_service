FROM python:3.12-slim

WORKDIR /app


COPY pyproject.toml poetry.lock ./


RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev

COPY . .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
