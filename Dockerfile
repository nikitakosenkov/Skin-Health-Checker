FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /code

ADD . /code/

RUN pip install -r requirements.txt

CMD python manage.py migrate \
&& python manage.py runserver
