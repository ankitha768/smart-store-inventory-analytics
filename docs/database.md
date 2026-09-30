# Database

SQLite is the default local-development database. MySQL is supported by setting DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST and DB_PORT in .env.

Run:
`python manage.py makemigrations`
`python manage.py migrate`
