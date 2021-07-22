FROM python:3.9-buster

EXPOSE 80

RUN pip install --upgrade pip
RUN pip install poetry --no-cache-dir
RUN pip install gunicorn
RUN poetry config virtualenvs.create false --local

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY website/zechcodes .

CMD ["gunicorn", "zechcodes.wsgi:application", "--bind", "0.0.0.0:80", "--workers", "3"]
