# start from a python 3.11 image
FROM python:3.11-slim

RUN python -m venv virtualenv
ENV PATH="/virtualenv/bin:$PATH"

# copy source files and install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src

# change to src directory and collect static files
WORKDIR /src

RUN python manage.py collectstatic

ENV DJANGO_DEBUG_FALSE=1
CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]