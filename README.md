# Requirements
- A working mysql setup
- A working redis setup
- python3.5
- nodejs

# Installation
## Database

Sqlite is not supported.
To create a mysql database, use:
```
CREATE DATABASE my_database CHARACTER SET utf8;
```


## Venv
```
pyvenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Dependency
```
npm install
```
During the installation process, npm ask you some informations to create the 'semantic.json' file
Choose express install and define installation path for semantic-ui to :
```
static/semantic/
```
Then, build the package by executing :
```
cd static/semantic/
gulp build
```

## Migrations
```
./manage.py migrate
```

## SuperUser creation
```
./manage.py createsuperuser
```

You should now be able to connect and admin the website !
