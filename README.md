# bmat-test
🎧 Code test for the Software Developer position at BMAT

## Backend Instructions

```
cd bmat_works/
```

### Setup database

#### Method 1: Docker

- Open terminal and run
```
docker run -it -p 5432:5432 -e POSTGRES_PASSWORD=jlram -e POSTGRES_USER=jlram -e POSTGRES_DB=jlworks -d postgres
```

#### Method 2: Local database

- Open terminal and open PostgreSQL shell (`sudo -u postgres psql`)
- Then create user, database and grant privileges:
```
CREATE USER jlram WITH PASSWORD 'jlram';
CREATE DATABASE jlworks;
GRANT ALL PRIVILEGES ON DATABASE jlworks TO jlram;
```

### Install dependencies

At this point, you should have created a virtual enviroment

```
pip install -r requirements.txt
```

### Apply migrations

```
python manage.py makemigrations works && python manage.py migrate
```

### Run

```
python manage.py runserver
```

Your API will be running at 127.0.0.1:8000

## Frontend Instructions

Move back to root and then 
```
cd bmat_frontend/
```

### Install dependencies

```
npm i
```

### Run
```
npm run serve
```

The Single View Application will be displayed at 127.0.0.1:8080