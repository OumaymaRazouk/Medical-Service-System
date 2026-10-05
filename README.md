# MedicalServiceSystem

Application Django de gestion des activités d'un service médical, avec MySQL.

## Configuration

La configuration publiée utilise les variables d'environnement suivantes :

- `DJANGO_SECRET_KEY` : clé privée obligatoire, différente pour chaque installation.
- `DJANGO_DEBUG` : `false` par défaut ; `true` uniquement en développement.
- `DJANGO_ALLOWED_HOSTS` : hôtes séparés par des virgules.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` : accès MySQL.

Pour générer une nouvelle clé : `python -c "import secrets; print(secrets.token_urlsafe(50))"`.
Définir les variables dans l'environnement du processus avant de lancer Django.
Un fichier `.env` n'est pas chargé automatiquement.

L'installation locale existante conserve sa configuration dans
`auth_project/settings_local.py`, ignoré par Git. Ce fichier a priorité sur les
variables d'environnement ; ne jamais le publier ni le copier en production.

## Vérification locale

Exécuter `python manage.py check` dans l'environnement Python du projet.
La procédure de réinstallation reste à valider : les migrations de l'application
`users` ont été supprimées dans la copie de travail. Ne pas appliquer de nouvelles
migrations sur une base existante sans vérifier son schéma et son historique.

## Publication GitHub

Ne jamais publier les données médicales, photos, bases de données, configurations
locales ou identifiants contenus dans `Prerequis.txt`.

Attention : l'ancien commit contient déjà des fichiers privés. Le `.gitignore`
n'efface pas les fichiers suivis ni l'historique. La publication nécessite un
nouveau dépôt sans cet historique, à partir d'une copie filtrée et vérifiée.
Conserver le dépôt original et les données locales comme sauvegarde.

Renouveler les clés et mots de passe qui ont été partagés ou enregistrés dans
l'ancien historique avant toute utilisation en production.
