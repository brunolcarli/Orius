FROM python:3.7-alpine

RUN apk add make
RUN apk add --no-cache gcc libc-dev git libffi-dev openssl-dev

RUN mkdir /usr/src/code
WORKDIR /usr/src/code

ENV PYTHONPATH /usr/src/code

COPY orius/requirements/common.txt .
RUN pip3 install -r common.txt

RUN apk del gcc libc-dev git libffi-dev openssl-dev

# Copia o restante do código depois de instalar as dependências para preservar a cache
COPY . .

ENV PYTHONUNBUFFERED 1
ENV NAME orius