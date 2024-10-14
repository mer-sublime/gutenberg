# gutenberg
A Django app for ingesting and querying French literature data from Gutendex

## Setup

1. Copy the example environment file and rename it:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your own values.

3. Run the project in the background with docker:
```bash
docker compose build --no-cache
docker compose up -d
```

4. Apply migrations on your fresh database:
```bash
docker compose run web python manage.py migrate 
```

5. Create your own superuser:
```bash
docker compose run web python manage.py createsuperuser
```

6. Go to http://localhost/admin/.

You should now be able to log in with your super user credentials.  
Congrats! The project is now up and running!

## Run
1. Run the project's containers in the background:
```bash
docker compose up -d
```

2. Run the following command to start populating the database with French Books and Authors
```bash
docker compose run web python manage.py fetch_books --pages 3 --start-page 1
```

3. Check the results of the Authors API by visiting http://localhost/api/authors/