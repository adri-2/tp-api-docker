FROM python:3.12-alpine


# 2. Installer les dépendances système utiles pour SQLite et Django

# 3. Créer le répertoire de travail
WORKDIR /tp-api

# 4. Copier les fichiers requirements
COPY requirements.txt .

# 5. Installer les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Copier le code source
COPY . .

# 7. Lancer le serveur avec Gunicorn

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
