# bmat-test
🎧 Code test for the Software Developer position at BMAT

## Instructions

### Setup database

- Open terminal and open PostgreSQL shell (`sudo -u postgres psql`)
- Then create user, database and grant privileges:
```
CREATE USER jlram WITH PASSWORD 'jlram';
CREATE DATABASE jlworks;
GRANT ALL PRIVILEGES ON DATABASE jlworks TO jlram;
```

### Run migrations

```
cd bmat_works
python manage.py makemigrations && python manage.py migrate
```