![Writing in the Margins](./public/images/logo.png)

# Writing in the Margins

Discuss your next good read

## What is it?

## Installation Instructions

1. Fork and clone this repository.

2. Set up a `.env` file and add the following:

- `NEXT_PUBLIC_HEROKU_SERVER_URL=https://spoti-chat-41fc1f2f3950.herokuapp.com`
- `NEXT_PUBLIC_LOCAL_SERVER_URL=http://localhost:8000`
- `SECRET_KEY = "YOUR_DJANGO_SECRET_KEY"`
- `DB_NAME = "YOUR_DB_NAME"`
- `DB_USER = "YOUR_DB_USER"`
- `DB_PASSWORD = "YOUR_DB_PASS"`
- `DB_HOST = "localhost"`
- `DB_PORT = 5432`
- `SCRAPEOPS_API_KEY = "YOUR_SCRAPEOPS_API_KEY"`

3. Run the following commands from your terminal while inside of the project's directory:

- `python3 manage.py runserver`
- `python manage.py tailwind start  `
- `./tailwindcss -i static/css/input.css -o static/css/output.css --watch`

# User Stories

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
