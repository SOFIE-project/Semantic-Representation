 
FROM  ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-pip

LABEL Author=filippo.vimini@aalto.com

WORKDIR /project

EXPOSE 5000

ENTRYPOINT [ "sh","/var/semantic-representation/boot.sh" ]