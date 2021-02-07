# bmat-test
🎧 Code test for the Software Developer position at [BMAT](https://www.bmat.com/)

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
ALTER ROLE jlram SUPERUSER;
```

### Install dependencies

At this point, you should have created a virtual enviroment, then run:

```
pip install -r requirements.txt
```

*Note: some dependencies might be needed for psycopg2, depending on your OS*

### Apply migrations

```
python manage.py makemigrations works && python manage.py migrate
```

### Test Endpoints

Probably you would need to modify permissions for `jlram` to run tests. In this case, open your PostgreSQL shell on Docker or locally and run:

```
ALTER USER jlram CREATEDB;
```

Once this is done, tests are ready to run:

```
python manage.py test
```

### Run API

```
python manage.py runserver
```

Your API will be running at `127.0.0.1:8000`

## Frontend Instructions

Move back to root and then to the Frontend directory
```
cd ../bmat_frontend/
```

### Install dependencies

```
npm i
```

### Run
```
npm run serve
```

## How it works

- Open the Single View Application at `127.0.0.1:8080`
- Press "Open CSV to load metadata" to upload your file
- Works will be displayed
- To perform a second upload, press X on the file input and then upload another (or the same) csv
- To export Works to another importable CSV file, press "Export Data to CSV"
- To retrieve a Work by its ISWC, navigate to `127.0.0.1:8000/<work_iswc>/`
- Every endpoint is listed at `127.0.0.1:8000`, including:
    - Work CRUD
    - Contributor CRUD
    - Source CRUD
    - Import CSV
    - Export CSV

## Questions

### 1. Describe briefly the matching and reconciling method chosen

As the ISWC is a unique code in the whole music industry, the first thing we do is checking if a Work with that ISWC already exists in our database. If it does not, we create a new Work.
If the Work we are reading from the .CSV does not contain an ISWC, we will save it in a backup array which will be iterated afterwards, to check if a song with the exact name and contributors exists. If they are not the same title or contributors, we are risking to be merging two different songs (The newer one could be a remix, for example)

If a song with that ISWC exists in our database, what we do is compare both the work from the .CSV and ours, using this criterion:

Title: All the different titles will be added to our song. For example, in Me enamoré/Me enamore are two versions of a song's title and both should be declared for non-Spanish speakers.

Contributors: The program reads every name from the contributor cell. If the current name does not exist, we create a new Contributor and add it to the Work contributors list (In Coldplay's Adventure of a Lifetime we merged the 4 names)
At first, I thought that if a name is strongly similar to another, the longer one should stay and the other one disappears. I could have developed a method, but I think we could lose information by doing this. For example, if we had a song by Julio Iglesias and a cover by Julio Iglesias Jr, Jr would have absorbed the first one.

Source and ID: Every different source and id will be added to our db. We want to do this because is interesting to have every source we receive our metadata from and the Work's id in their database.

### 2. We constantly receive metadata from our providers, how would you automatize the process?
Python is a very strong and volatile language. In my opinion, a good idea would be to create an endpoint that Sources use to send us their data, and constantly add the data to a formatted .CSV file. I also would implement a cron job that calls our `import_csv` endpoint every hour (for example) with that clean formatted .CSV file, to prevent massive changes to our database be constantly done.

### 3. Imagine that the Single View has 20 million musical works, do you think your solution would have a similar response time?
Not at all.

### 4. If not, what would you do to improve it?
Implement pagination with Django Rest and Vue.js' datatable, so the user receives 100 songs at once, and every time they click ➡️ on the datatable, another 100 songs load. Also, a good idea for that amount of songs would be implementing `django-rest-framework-filters` to get a more concise list of Works, depending on the user's interests.
