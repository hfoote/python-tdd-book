FROM python:3.11-slim

RUN python -m venv /virtualenv
ENV PATH="/virtualenv/bin:$PATH"

RUN pip install "django==5.1.4"

COPY src /src

WORKDIR /src

CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]