![Writing in the Margins](./public/images/logo.png)

# Writing in the Margins

Discuss your next good read

## What is it?

## Installation Instructions

1. Fork and clone this repository.

2. Set up a `.env` file and add the following:

- `SECRET_KEY = "YOUR_DJANGO_SECRET_KEY"`
- `DB_NAME = "YOUR_DB_NAME"`
- `DB_USER = "YOUR_DB_USER"`
- `DB_PASSWORD = "YOUR_DB_PASS"`
- `DB_HOST = "localhost"`
- `DB_PORT = 5432`
- `SCRAPEOPS_API_KEY = "YOUR_SCRAPEOPS_API_KEY"`

3. Run the following commands from your terminal while inside of the project's directory:

1. &emsp;`python -m pip install -r requirements.txt`

1. &emsp;On your PostgresSQL create a database with the schema.sql included on this project.

1. &emsp;Depending on how your PostgreSQL is setup, you might have to edit the values on the .env file. This file usually should be not included in repositories since it contains sensitive information but since this is mainly for demonstration adding the file shouldn't be a big deal.

1. &emsp;`cd bookclub`

1. &emsp;`python manage.py makemigrations`

1. &emsp;`python manage.py migrate`

1. &emsp;`python manage.py crawl`

1. &emsp;`python manage.py runserver`

1. &emsp;`python3 manage.py runserver`

1. &emsp;`python manage.py tailwind start`

1. &emsp;`./tailwindcss -i static/css/input.css -o static/css/output.css --watch`

## User Stories

- As a user I can create an account
- As a user I can view and edit my profile information
  - Stretch Goal: Allow users to upload profile photos
- As a user I search for and view book data
- As a user I can add books to read, currently reading, want to read, and watch lists
- As a user I can join a book club
  - Stretch Goal: Allow users to create their own book club
- As a user I can participate in book discussions
  - Users can create new responses and delete their own responses
- As a user I can choose bookclub books (admin) or suggest books (non-admin)

BIG STRETCH GOAL:

- Email users when price drops below watch list price

## DATABASE ERD

## WIREFRAMES

## STACK USED

- Django
- Postgres
- Tailwind CSS
- Scrapy
- ScrapeOps

# Challenges

- Changing the class/styling of a dynamically generated element
- Implementing a loading screen while the spider runs
