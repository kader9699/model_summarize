# Utiliser une image Python de base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt ./
COPY app.py ./
#COPY model ./model/


# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel Streamlit s'exécute
EXPOSE 8501

# Commande pour démarrer Streamlit
CMD ["streamlit", "run", "app.py"]
