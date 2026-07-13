# Cloudflare Turnstile Setup

This project already contains the backend and frontend integration for Cloudflare Turnstile on the contact form.

## What is already implemented

- Hidden honeypot field for simple bot submissions
- Signed form token with minimum fill time
- Optional Cloudflare Turnstile widget on the contact page
- Server-side token verification against Cloudflare

Turnstile is only enabled when both environment variables below are set.

## Required environment variables

Set these variables in the production environment:

```bash
TURNSTILE_SITE_KEY=your_site_key
TURNSTILE_SECRET_KEY=your_secret_key
```

## Cloudflare dashboard steps

1. Log in to Cloudflare.
2. Open `Turnstile`.
3. Create a new widget.
4. Choose the domain names:
   - `datalization.ch`
   - `www.datalization.ch`
5. Copy the generated `site key` and `secret key`.

Recommended widget mode:

- `Managed`

## Heroku example

If the site is deployed on Heroku, set the config vars:

```bash
heroku config:set TURNSTILE_SITE_KEY=your_site_key
heroku config:set TURNSTILE_SECRET_KEY=your_secret_key
```

After setting the variables, deploy or restart the app.

## Local testing

You can also enable Turnstile locally by exporting the same variables before starting Django.

```bash
export TURNSTILE_SITE_KEY=your_site_key
export TURNSTILE_SECRET_KEY=your_secret_key
python3 manage.py runserver
```

## Files involved

- `datalization_site/settings.py`
- `web/views.py`
- `web/templates/contact.html`
- `web/static/js/main.js`
- `web/tests.py`
