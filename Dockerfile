 
FROM python:3.7-alpine

LABEL Author=filippo.vimini@ericsson.com

WORKDIR /var

COPY . /var

RUN pip3 install -r /var/app/requirements.txt

RUN chmod +x /var/boot.sh 

EXPOSE 5000

ENTRYPOINT [ "sh","/var/boot.sh" ]