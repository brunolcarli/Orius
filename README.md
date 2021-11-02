<table align="center"><tr><td align="center" width="9999">

<img src="https://opengameart.org/sites/default/files/styles/medium/public/cutewizard.png" align="center" width="170" alt="Project icon">

# Orius

*Discord RPG bot*

</td></tr>

</table>    

<div align="center">

> [![Version badge](https://img.shields.io/badge/version-1.4.5-silver.svg)]()
[![Docs Link](https://badgen.net/badge/docs/github_wiki?icon=github)](https://github.com/brunolcarli/Orius/wiki)
[![Add to discord](https://badgen.net/badge/icon/discord?icon=discord&label)](https://discord.com/api/oauth2/authorize?client_id=776075554817310730&permissions=1074261056&scope=bot)


Discord Bot for Role Playing Game such as leveling up, skill gathering and guild member battles!

[Add to your discord server](https://discord.com/api/oauth2/authorize?client_id=776075554817310730&permissions=1074261056&scope=bot)

</div>


## Developers

### Cloning and executing

![Linux Badge](https://img.shields.io/badge/OS-Linux-black.svg)
![Apple badge](https://badgen.net/badge/OS/OSX/:color?icon=apple)


#### Local machine

First of all you must have a instance of MongoDB running on your machine, so if you
dont have a mongodb go to [mongo installation guide](https://docs.mongodb.com/manual/installation/) and install MongoDB.

Clone this project and engage a **python3** virtual environment the way as you like and install the requirements through Makefile.

Example using virtualevwrapper:

```
$ git clone https://github.com/brunolcarli/Orius.git
$ cd Orius/
$ mkvirtualenv Orius
$ (Orius) make install
```

Now create a enviroment file based on the template available in `orius/environment/template` and create yours with your own environment variables. Assuming you create a file called `foo_env`, add the following variables:

> *you may need to create a user on database for this.*

```
export TOKEN=your_bot_token
export MYSQL_HOST=localhost
export MYSQL_USER=orius
export MYSQL_PASSWORD=orius_pwd
export MYSQL_DATABASE=orius
```

and export these variables:

```
$ source foo_env
```

Run the migrations to create database tables and populating with the skills listed on `orius/skills.json`.

```
$ make migrate
```

Run the bot through Makefile:

```
$ make run
```

## Docker

Install docker-compose through `pip`:

```
$ pip install docker-compose
```

Create a environment file called `orius_env` at `orius/environment/orius_env` and put the environment variables with your own values on it, based on the template available at `orius/environment/docker_template`.

Compile and run the docker containers with docker-compose:

```
$ docker-compose build
$ docker compose up
```

Note: If you want the container to run background run `docker-compose up -d`

You must create a user and password for your mongo client user. Find the container hash id with:

```
$ docker ps -a | grep orius
```

It shoold return something like:

```
69a8b08fbb58  orius:devel  "make run"    50 minutes ago      Up 8 minutes      orius_container                                                                                                
13a1fcf31874  mongo   "docker-entrypoint.s…"   58 minutes ago      Up 8 minutes           27017/tcp          orius_mongo_1
```

The one youre looking for is the hash for `orius_mongo`, in this case it is `13a1fcf31874`.

Call a mysql shell from docker container:

```
$ docker exec -ti 13a1fcf31874 mysql
```

Create a new user with root role for your access

```
mysql> CREATE USER 'orius'@'localhost' IDENTIFIED BY '<password>';
mysql> GRANT ALL PRIVILEGES ON * . * TO 'orius'@'localhost';
```


Run the migrations:

```
$ docker exec -ti 13a1fcf31874 make migrate
```


#### See also:

- [Noob guide: running on local machine](https://github.com/brunolcarli/Orius/wiki/Noob-Guide:-Develop-and-run)