FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    apt-get install make

RUN apt-get update && apt-get install -y python3-pip

# mongo
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
RUN sudo apt-get install gnupg
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

RUN sudo apt-get update
RUN sudo apt-get install -y mongodb-org

RUN mkdir /app
WORKDIR /app

COPY orius/requirements/common.txt .

RUN pip3 install -r common.txt


COPY . .
ENV LANG C.UTF-8
ENV NAME orius