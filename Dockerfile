FROM ubuntu:18.04

LABEL Author=filippo.vimini@ericsson.com

RUN apt-get update && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

EXPOSE 5000

CMD ["api/sr_interface.py"]

