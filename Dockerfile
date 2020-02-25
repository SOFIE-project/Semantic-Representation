 
FROM python:3.7-alpine

LABEL Author=filippo.vimini@aalto.com

WORKDIR /project

EXPOSE 5000

ENTRYPOINT [ "sh","/var/boot.sh" ]