# Credit Group Technical Challenge - Backend

## Flask app

It contains a Flask app which resolve the following objective:

> Bulid a web service which exposes the current exchange
> rate of USD to MXN from three different sources in the same endpoint.
> The response format should be something like the following:

> ```json
> "rates": {
>     "provider_1": {
>         "last_updated": "2018-04-22T18:25:43.511Z",
>         "value": 20.4722
>     },
>     "provider_2_variant_1": {
>         "last_updated": "2018-04-23T18:25:43.511Z",
>         "value": 20.5281
>     }
> }
> ```

> Exchange rate sources:
>
> - [Diario Oficial de la Federación](https://www.banxico.org.mx/tipcamb/tipCamMIAction.do) - No API provided, so you will need to scrape the site
> - [Fixer](https://fixer.io/) - Well documented API in JSON format
> - [Banxico](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/consultaDatosSerieRango) - Service SF43718. API returns XML.

## Docker Deployment in Heroku

Heroku CLI needed.
The Flask app is containerized using Docker, so to deploy the app in a production environment it is recommended to use Gunicorn (see src/Dockerfile).

1. Clone the repo, checkout to the "develop" branch and login into Heroku CLI:

```sh
git clone https://github.com/luks04/cg_technical_challenge_backend.git
cd cg_technical_challenge_backend
git checkout develop
heroku login
```

2. Delete Heroku remote old repository:

```sh
git remote rm heroku
```

3. Check remote repositories:

```sh
git remote -v
```

4. Deploy the app with a Dockerfile using heroku.yml:

```sh
heroku create <app_name>
heroku stack:set container
git push heroku <source_branch>:main
```

5. Deploy new changes:

```sh
git add .
git commit -m "<commit message>"
git push heroku <source_branch>:main
```

6. To show the logs use the next command:

```sh
heroku logs --tail
```
