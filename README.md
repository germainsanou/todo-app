# Todo App

Template de projet : Django (API) + Vue.js (interface), déployé en monolithe avec Docker.
L'authentification est prête pour un frontend web **et** une application mobile.

## Développement local

Backend :
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements/local.txt
python manage.py migrate
python manage.py createsuperuser   # accès à /admin/ (connexion par email)
python manage.py runserver
```

Frontend (dans un second terminal) :
```bash
cd frontend
npm install
npm run dev
```

Ouvrir http://localhost:5173.

Emails (codes de vérification, mot de passe oublié) : lancer [MailDev](https://github.com/maildev/maildev)
dans un troisième terminal avec `npx maildev`, puis consulter http://localhost:1080.
Django l'attend sur `localhost:1025` (modifiable avec `DJANGO_EMAIL_HOST` / `DJANGO_EMAIL_PORT`).

Tests :
```bash
cd backend
python manage.py test --settings=config.settings.test
```

## Avec Docker

```bash
cp .env.example .env   # puis remplir les valeurs
docker compose up --build -d
```

Ouvrir http://localhost:8000. Les emails envoyés sont visibles dans MailDev : http://localhost:1080
(arrêter au préalable un éventuel `npx maildev`, qui utilise les mêmes ports).

## Organisation du backend

```
backend/
├── config/                  # configuration du projet
│   ├── settings/
│   │   ├── base.py          # réglages communs
│   │   ├── local.py         # développement (défaut de manage.py)
│   │   ├── test.py          # tests
│   │   └── production.py    # production (défaut de wsgi.py, utilisé par Docker)
│   ├── urls.py              # URL racine
│   ├── api_router.py        # routes de l'API REST (/api/v1/)
│   └── views.py             # sert l'application Vue.js
├── apps/                    # une app Django par domaine métier
│   ├── users/               # modèle User personnalisé (connexion par email)
│   └── todos/
│       ├── models.py
│       ├── admin.py
│       ├── api/             # serializers.py, views.py
│       ├── migrations/
│       └── tests/
└── requirements/            # base.txt, local.txt, production.txt
```

Pour ajouter un domaine : `mkdir apps/factures && python manage.py startapp factures apps/factures`,
puis mettre `name = "apps.factures"` dans `apps.py`, l'ajouter à `LOCAL_APPS`
et enregistrer ses vues dans `config/api_router.py`.

## Authentification

Gérée par [django-allauth](https://docs.allauth.org/) en mode *headless* (API uniquement) :

- inscription et connexion par **email + mot de passe** ;
- **vérification de l'email obligatoire** par un code envoyé par email ;
- mot de passe oublié par code ;
- limitation des tentatives et protection contre l'énumération des comptes ;
- mots de passe validés par les validateurs Django.

| Client | Endpoints d'authentification | Authentification des appels à `/api/v1/` |
|---|---|---|
| Frontend web (Vue.js) | `/_allauth/browser/v1/…` | cookie de session HttpOnly + en-tête `X-CSRFToken` |
| Application mobile | `/_allauth/app/v1/…` | en-tête `X-Session-Token` |

Côté web, aucun jeton n'est stocké dans le navigateur : le cookie de session est
inaccessible au JavaScript, ce qui protège contre le vol de session par XSS.

Toutes les routes de `/api/v1/` exigent par défaut un utilisateur connecté
(`IsAuthenticated`). Pour une route publique, déclarer
`permission_classes = [AllowAny]` sur la vue.

Documentation interactive (en développement uniquement) :
- authentification : http://localhost:8000/_allauth/openapi.html
- API métier : http://localhost:8000/api/docs/

### Brancher une application mobile

1. `POST /_allauth/app/v1/auth/signup` avec `{"email", "password"}`. La réponse 401
   indique l'étape en attente `verify_email` et contient `meta.session_token`.
2. `POST /_allauth/app/v1/auth/email/verify` avec `{"key": "<code reçu>"}` et
   l'en-tête `X-Session-Token`. Une réponse 200 signifie que l'utilisateur est connecté.
3. Plus tard, `POST /_allauth/app/v1/auth/login` avec `{"email", "password"}`
   renvoie `meta.session_token`.
4. Appeler l'API avec `X-Session-Token: <token>`, par exemple `GET /api/v1/users/me/`.
5. Pour se déconnecter : `DELETE /_allauth/app/v1/auth/session`.

Stocker le jeton dans le stockage sécurisé du téléphone (Keychain / Keystore).
Les apps natives ne sont pas soumises au CORS : aucune configuration
supplémentaire n'est nécessaire. Seul un frontend web servi depuis **un autre
domaine** demanderait `django-cors-headers`.

## Production

Variables à définir dans le `.env` du serveur (voir `.env.example`) :
`DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`,
`DATABASE_URL`, les variables `DJANGO_EMAIL_*` du serveur SMTP, et
`DJANGO_SECURE_HSTS_SECONDS=31536000` une fois le HTTPS en place.

## Contribuer

Ne jamais pousser sur `main` : une branche par tâche, puis une Pull Request.
