FROM python:3.11-slim

RUN python -m venv /virtualenv
ENV PATH="/virtualenv/bin:$PATH"

RUN pip install "django==5.1.4" "gunicorn==23.0.0" "whitenoise==6.9.0"

COPY src /src

WORKDIR /src

CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]