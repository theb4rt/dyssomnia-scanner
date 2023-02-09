# Dyssomnia

Clone repository

```
git clone REPOSITORY_URL
```

Create .env file

```
cp .env.example .env
```

Modify env variables into the .env file

Build docker image with docker-compose

```
docker-compose build -d
```

Execute migrations

```
flask db stamp
flask db migrate
flask db upgrade
```

Execute migrations after change models

```
flask db migrate
flask db upgrade
```

If you see the message **"Error: Can't locate revision identified by '[some_id]'"**,
use the command

`"flask db revision --rev-id [some_id]"`

and then execute the commands

```
flask db migrate
flask db upgrade
```

Execute seeders to populate database

```
flask seed run --root=./ms/db/seeders
```

Run tests

```
coverage run -m pytest
```
