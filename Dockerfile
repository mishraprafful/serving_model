FROM  ubuntu
LABEL MAINTAINER Prafful Mishra mishraprafful@gmail.com

RUN mkdir -p /model_server/app/
WORKDIR /model_server/app/

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 --no-cache-dir install --upgrade pip

RUN python -m pip install --upgrade setuptools wheel

COPY ./ /model_server/

RUN pip install -r requirements.txt

ENTRYPOINT ["flask","run","-h","0.0.0.0"] 