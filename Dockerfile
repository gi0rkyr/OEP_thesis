FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBUG True

WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/

#RUN apt-get update && apt-get install -y \
 # uwsgi \
  #uwsgi-plugin-python3 

#RUN cp /usr/lib/uwsgi/plugins/python3_plugin.so /code/

#EXPOSE 81

#CMD ["python", "manage.py", "runserver"]