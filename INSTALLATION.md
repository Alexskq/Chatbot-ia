# Guide d'Installation et d'Utilisation du Projet ChatBot IA

Ce guide vous aidera à installer et à exécuter le projet ChatBot IA sur votre ordinateur. Suivez ces étapes dans l'ordre pour une installation réussie.

## Méthode 1 : Installation Automatique (Recommandée)

Pour une installation simplifiée, vous pouvez utiliser les scripts d'installation automatique inclus dans le projet.

### Sur Windows

1. Ouvrez l'Explorateur de fichiers et naviguez jusqu'au dossier du projet
2. Double-cliquez sur le fichier `install_windows.bat`
3. Suivez les instructions à l'écran

### Sur Mac/Linux

1. Ouvrez un Terminal
2. Naviguez jusqu'au dossier du projet : `cd chemin/vers/le/dossier/chatbot_ia`
3. Rendez le script exécutable (si ce n'est pas déjà fait) : `chmod +x install_unix.sh`
4. Exécutez le script : `./install_unix.sh`
5. Suivez les instructions à l'écran

### Utilisation du script Python (Alternative)

Si les scripts ci-dessus ne fonctionnent pas, vous pouvez utiliser le script Python :

1. Ouvrez un terminal (Invite de commandes sur Windows, Terminal sur Mac/Linux)
2. Naviguez jusqu'au dossier du projet : `cd chemin/vers/le/dossier/chatbot_ia`
3. Exécutez le script d'installation :
   - Sur Windows : `python setup.py`
   - Sur Mac/Linux : `python3 setup.py`
4. Suivez les instructions à l'écran

Les scripts vous guideront à travers toutes les étapes d'installation et de configuration.

## Méthode 2 : Installation Manuelle

Si vous préférez installer le projet manuellement, suivez les étapes ci-dessous.

### Prérequis

Avant de commencer, assurez-vous d'avoir installé les logiciels suivants sur votre ordinateur :

1. **Python 3.10 ou plus récent** : [Télécharger Python](https://www.python.org/downloads/)
2. **PostgreSQL** : [Télécharger PostgreSQL](https://www.postgresql.org/download/)
3. **Git** (optionnel) : [Télécharger Git](https://git-scm.com/downloads)

### Étape 1 : Télécharger le projet

Si vous avez reçu le projet sous forme d'archive ZIP, décompressez-le dans un dossier de votre choix.

Si vous utilisez Git, vous pouvez cloner le dépôt avec la commande :
```
git clone [URL_DU_DEPOT]
```

### Étape 2 : Configurer l'environnement virtuel Python

Ouvrez un terminal (Invite de commandes sur Windows, Terminal sur Mac/Linux) et naviguez jusqu'au dossier du projet :

```
cd chemin/vers/le/dossier/chatbot_ia
```

Créez un environnement virtuel Python :

Sur Windows :
```
python -m venv venv
venv\Scripts\activate
```

Sur Mac/Linux :
```
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les dépendances

Une fois l'environnement virtuel activé, installez les dépendances du projet :

```
pip install -r requirements.txt
```

### Étape 4 : Configurer la base de données PostgreSQL

Vous pouvez configurer la base de données de deux façons :

#### Option A : Utiliser le script SQL fourni (recommandé)

1. Assurez-vous que PostgreSQL est installé et en cours d'exécution
2. Ouvrez un terminal et exécutez la commande suivante :

Sur Windows :
```
psql -U postgres -f database_setup.sql
```

Sur Mac/Linux :
```
sudo -u postgres psql -f database_setup.sql
```

#### Option B : Configuration manuelle

1. Ouvrez pgAdmin (interface graphique de PostgreSQL) ou utilisez l'outil en ligne de commande.
2. Créez une nouvelle base de données nommée `chatbot_db`.
3. Créez un nouvel utilisateur PostgreSQL avec les informations suivantes :
   - Nom d'utilisateur : `alex`
   - Mot de passe : `coucou`
   - Droits : Tous les droits sur la base de données `chatbot_db`

Si vous préférez utiliser vos propres identifiants, vous devrez modifier le fichier `chatbot_ia/settings.py` pour mettre à jour les informations de connexion à la base de données.

### Étape 5 : Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet avec le contenu suivant :

```
OPENAI_API_KEY=votre-clé-api-openai
```

Pour obtenir une clé API OpenAI :
1. Créez un compte sur [OpenAI](https://platform.openai.com/signup)
2. Accédez à la section API Keys
3. Créez une nouvelle clé API
4. Copiez cette clé dans le fichier `.env`

### Étape 6 : Initialiser la base de données

Exécutez les migrations pour créer les tables dans la base de données :

```
python manage.py migrate
```

Créez un superutilisateur pour accéder à l'interface d'administration :

```
python manage.py createsuperuser
```

Suivez les instructions pour créer un compte administrateur.

### Étape 7 : Lancer le serveur

Démarrez le serveur de développement :

```
python manage.py runserver
```

Le serveur démarre à l'adresse http://127.0.0.1:8000/

## Utilisation de l'Application

1. Ouvrez votre navigateur et accédez à http://127.0.0.1:8000/
2. Connectez-vous avec le compte superutilisateur que vous avez créé
3. Vous pouvez maintenant explorer l'application :
   - Créer des simulations
   - Interagir avec le chatbot
   - Consulter les analyses

## Résolution des problèmes courants

### Erreur de connexion à la base de données
- Vérifiez que PostgreSQL est bien démarré
- Vérifiez les identifiants dans le fichier `settings.py`
- Assurez-vous que la base de données `chatbot_db` existe

### Erreur avec l'API OpenAI
- Vérifiez que votre clé API est correcte dans le fichier `.env`
- Assurez-vous que votre compte OpenAI est actif et dispose de crédits

### Le serveur ne démarre pas
- Vérifiez que toutes les dépendances sont installées
- Assurez-vous que l'environnement virtuel est activé
- Vérifiez les logs d'erreur dans le terminal

Pour toute autre question ou problème, n'hésitez pas à contacter le développeur. 