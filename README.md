# GUDLFT Registration & Booking System

Bienvenue dans le projet GUDLFT Registration & Booking System. Ce projet est une application web qui permet aux clubs de fitness de s'enregistrer, de se connecter, et de réserver des places pour des compétitions. Le système gère les compétitions, les clubs et leurs points pour faciliter les réservations et l'organisation d'événements sportifs.

## Fonctionnalités principales 
- **Enregistrement et connexion des clubs :** Les clubs peuvent créer un compte avec leur nom, email, et un mot de passe sécurisé.
- **Réservation de places pour des compétitions :** Les clubs peuvent réserver des places dans différentes compétitions sportives, sous réserve des places disponibles et de leurs points.
- **Gestion des points des clubs :** Les clubs disposent d'un certain nombre de points à dépenser pour réserver des places dans les compétitions.
- **Affichage des compétitions actuelles :** Seules les compétitions futures (dont la date n'est pas encore passée) sont affichées sur la page d'accueil.
- **Pagination des compétitions :** Système de pagination pour naviguer parmi les nombreuses compétitions.


## Prérequis
Liste des dépendances utilisées dans le projet (extrait du ```requirements.txt```) :
```
blinker==1.8.2
Brotli==1.1.0
certifi==2024.8.30
charset-normalizer==3.3.2
click==8.1.7
ConfigArgParse==1.7
coverage==7.6.3
datetype==2024.2.28
flake8==7.0.0
flake8-html==0.4.3
Flask==3.0.3
Flask-Cors==5.0.0
Flask-Login==0.6.3
gevent==24.2.1
geventhttpclient==2.3.1
greenlet==3.1.1
idna==3.10
iniconfig==2.0.0
itsdangerous==2.2.0
Jinja2==3.1.3
locust==2.31.8
MarkupSafe==2.1.5
mccabe==0.7.0
msgpack==1.1.0
npm==0.1.1
optional-django==0.1.0
packaging==24.1
pillow==10.3.0
pluggy==1.5.0
psutil==6.0.0
pycodestyle==2.11.1
pyflakes==3.2.0
Pygments==2.17.2
pytest==8.3.3
pytest-flask==1.3.0
pytest-mock==3.14.0
python-slugify==8.0.4
pyzmq==26.2.0
requests==2.32.3
setuptools==75.1.0
text-unidecode==1.3
urllib3==2.2.3
Werkzeug==3.0.4
zope.event==5.0
zope.interface==7.0.3
```


## Installation
### Cloner le projet :

```
git clone https://github.com/TombeEtoile/opcr_project_11.git
```
### Se rendre sur le projet
```
cd opcr_project_11
```
### puis
```
cd Python_Testing
```

### Installer les dépendances :
```
pip install -r requirements.txt
```

### Configurer les bases de données JSON :

Assurez-vous que les fichiers clubs.json et competitions.json sont présents dans le répertoire racine pour stocker les informations sur les clubs et les compétitions.

#### Exemple de contenu de clubs.json :
``` json
{
  "clubs": [
    {
      "name": "Nom Club",
      "email": "nomclub@gmail.com",
      "points": 12,
      "password": "$2b$12$h...hashé" 
    }
  ]
}
```
#### Exemple de contenu de competitions.json :
``` json
{
  "competitions": [
    {
      "name": "Nom Competition",
      "date": "2024-10-30 14:56",
      "available_places": 25
    }
  ]
}
```

## Exécution de l'Application

### Lancer le serveur Flask :
(route = /opcr_project_11/Python_Testing/)
```
flask run
```
L'application sera disponible à l'adresse http://127.0.0.1:5000.

### Naviguer sur l'application :

#### /
Connexion et enregistrement
#### /competition_registration
Mise en ligne d'une ccompétition
#### /homepage
Homepage (affichage de toutes les compétitions à venir)
#### /clubs
Liste de tous les clubs
#### /< nom-competition>/< nom-club>
Page de réservation de la compétition ciblée dans l'url
#### /logout
Page de déconnexion (302 --> "/")


## Tests

### Tests Unitaires (Pytest)
#### Exécuter les tests unitaires :

```
pytest
```

### Couverture des tests :

#### Couverture des tests en format txt :

```
coverage report
```

#### Visualiser la couverture des tests :
```
coverage html
```
Ensuite, ouvrez htmlcov/index.html dans votre navigateur pour une analyse détaillée.

### Tests de Performance (Locust)
Exécuter Locust pour tester les performances :
```
locust
```
Puis ouvrez votre navigateur et accédez à **http://localhost:8089** pour interagir avec l'interface Locust.

### Exemple de script Locust
Un exemple de test Locust est fourni dans le fichier ```locustfile.py``` à la racine du projet pour tester les routes de connexion, d'enregistrement et de réservation.
