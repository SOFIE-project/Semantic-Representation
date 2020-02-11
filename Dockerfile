FROM ubuntu:18.04

LABEL Author=filippo.vimini@ericsson.com

RUN apt-get update && \
    apt-get install -y python3-pip python3

WORKDIR /var

COPY . /var

RUN pip3 install -r /var/app/requirements.txt

ENTRYPOINT ["python3"]

EXPOSE 5000

CMD ["semantic_representation.py"]

