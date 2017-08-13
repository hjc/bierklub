# Bier Klub

Bier Klub is the public-facing event and invitation system for HJC's NYC Beer
Club.

To be hosted soon!

## Getting Started

Bier Klub is dockerized, so getting started is easy. First, add this line to
your hosts file (`/etc/hosts`):

```
127.0.0.1 bierklub.dev
```

Now, run the migrations: `cd bierklub && python manage.py migrate`.

Now, let's set up our static files: `cd bierklub && python manage.py
collectstatic`.

After that's done, just run `docker-compose up` and then visit `bierklub.dev`.
You should be good to go!

## Topics to Learn

* Creating your own models.
* Model managers.
* Custom querysets.
* Template extensions and the templating engine.
* Django Rest Framework
* More to come!
