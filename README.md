# Todo App

Application de gestion de tâches : Django (API) + Vue.js (interface), déployée en monolithe avec Docker.

## Développement local

Backend :
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend (dans un second terminal) :
```bash
cd frontend
npm install
npm run dev
```

Ouvrir http://localhost:5173

## Avec Docker

```bash
cp .env.example .env   # puis remplir les valeurs
docker compose up --build -d
```

Ouvrir http://localhost:8000

## Contribuer

Ne jamais pousser sur `main` : une branche par tâche, puis une Pull Request.