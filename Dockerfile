# ============ Étape 1 : compiler Vue.js ============
FROM node:24-alpine AS frontend

WORKDIR /app/frontend

# On copie d'abord les fichiers de dépendances seuls (pour le cache, voir plus bas)
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Puis le reste du code, et on compile
COPY frontend/ ./
RUN npm run build


# ============ Étape 2 : image finale Django ============
FROM python:3.14-slim

# Pas de fichiers .pyc, et logs affichés immédiatement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/backend

# Dépendances Python (même principe de cache)
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Code Django
COPY backend/ ./

# On récupère UNIQUEMENT le build Vue.js de l'étape 1
COPY --from=frontend /app/frontend/dist /app/frontend/dist

# Rassembler les fichiers statiques
RUN python manage.py collectstatic --noinput

# Ne pas faire tourner l'application en root (sécurité)
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Au démarrage : appliquer les migrations, puis lancer Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3"]