<table align="center"><tr><td align="center" width="9999">

<img src="https://opengameart.org/sites/default/files/styles/medium/public/cutewizard.png" align="center" width="170" alt="Project icon">

# Orius

*Discord RPG bot*

</td></tr>

</table>    

<div align="center">

> [![Version badge](https://img.shields.io/badge/version-0.0.1-silver.svg)]()
[![Docs Link](https://badgen.net/badge/docs/github_wiki?icon=github)](https://github.com/brunolcarli/Orius/wiki)


Discord Bot for Role Playing Game such as leveling up, skill gathering and guild member battles!

</div>


## Developers

### Cloning and executing

![Linux Badge](https://img.shields.io/badge/OS-Linux-black.svg)
![Apple badge](https://badgen.net/badge/OS/OSX/:color?icon=apple)


#### Local machine

Clone this project and engage a **python3** virtual environment the way as you like and install the requirements through Makefile.

Example using virtualevwrapper:

```
$ git clone https://github.com/brunolcarli/Orius.git
$ cd Orius/
$ mkvirtualenv Orius
$ (Orius) make install
```

Now create a enviroment file based on the template available in `orius/environment/template` and create yours with your own environment variables. Assuming you create a file called `foo_env`, add the following variables:

```
export TOKEN=your_bot_token
export MONGO_DATABASE=your_database_name
export MONGO_HOST=your_database_host
export MONGO_PORT=your_database_port
```

and export these variables:

```
$ source foo_env
```

Run the bot through Makefile:

```
$ make run
```