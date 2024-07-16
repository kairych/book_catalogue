# READ ME

## Book catalogue

### Launching an app
Clone project from GitHub:\
`git clone https://github.com/kairych/book_catalogue.git`

Install virtual environment:\
`python3 -m venv venv`

Activate virtual environment (Linux/Unix):\
`source venv/bin/activate`

Activate virtual environment (Windows):\
`venv\Scripts\activate`

Install all dependencies:\
`pip install -r requirements.txt`

Make migrations to create database:\
`./manage.py makemigrations`

Apply migrations:\
`./manage.py migrate`

Load test data to your database:\
`./manage.py dumpdata fixtures/accounts_dump.json fixtures/books_dump.json`

Change .env.example file to .env and set your email host name and email app password to send verification emails.

To run server:\
`./manage.py runserver`

To stop server:\
`ctrl + c`

API Documentation is available at:\
[Swagger UI](http://localhost:8000/swagger/)
or
[Redoc UI](http://localhost:8000/redoc/)


Test data can be added via Django Admin.

### Test users
Admin user (superuser)\
email: admin@mail.com\
password: admin123

Second user\
email: mail@mail.com
password: poiupoiu