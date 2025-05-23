FROM python:3.11-slim

RUN python -m venv /virtualenv
ENV PATH="/virtualenv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src

WORKDIR /src

CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]