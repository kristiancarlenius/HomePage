# Carlenius AI

Source for [carleniusai.no](https://carleniusai.no).

## Structure

- `index.html` and the images/logo next to it are the public site.
- `portal/` is a small internal Django app for the team: shared calendar, customer notes, hours/billing, and a repo directory. Lives at `/app/` on the same domain.

## Running the portal locally

```bash
cd portal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Without a `.env`, it falls back to SQLite and a dev-only secret key, fine for running locally.

## Deploying

Production needs a real `.env` (see `.env.example`), Postgres, and Gunicorn behind nginx at `/app/`. Passwords are hashed by Django, never stored in plain text, and `.env` is gitignored so nothing secret ends up in this repo.
