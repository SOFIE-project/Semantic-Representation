 
FROM python:3.7-alpine

LABEL Author=filippo.vimini@ericsson.com

WORKDIR /app

EXPOSE 5000

ENTRYPOINT [ "sh","/var/boot.sh" ]