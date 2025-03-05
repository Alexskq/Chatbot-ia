@echo off
echo ===============================================================================
echo                     Installation du Projet ChatBot IA (Windows)
echo ===============================================================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.10 ou plus récent depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Créer l'environnement virtuel
echo.
echo Création de l'environnement virtuel Python...
if exist venv (
    echo L'environnement virtuel existe déjà.
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERREUR: Impossible de créer l'environnement virtuel.
        pause
        exit /b 1
    )
    echo Environnement virtuel créé avec succès.
)

REM Activer l'environnement virtuel et installer les dépendances
echo.
echo Installation des dépendances...
call venv\Scripts\activate
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERREUR: Impossible d'installer les dépendances.
    pause
    exit /b 1
)
echo Dépendances installées avec succès.

REM Configurer le fichier .env
echo.
echo Configuration du fichier .env...
if exist .env (
    echo Le fichier .env existe déjà.
    set /p modify=Voulez-vous le modifier ? (o/n): 
    if /i "%modify%" neq "o" goto :database_setup
)

echo Entrez votre clé API OpenAI:
set /p api_key="> "
echo OPENAI_API_KEY=%api_key%> .env
echo Fichier .env créé avec succès.

:database_setup
REM Configuration de la base de données
echo.
echo Configuration de la base de données PostgreSQL...
echo.
echo Pour configurer la base de données PostgreSQL, vous avez deux options:
echo.
echo 1. Utiliser le script SQL fourni (recommandé)
echo    Exécutez la commande: psql -U postgres -f database_setup.sql
echo.
echo 2. Configuration manuelle
echo    - Créer une base de données nommée 'chatbot_db'
echo    - Créer un utilisateur PostgreSQL 'alex' avec mot de passe 'coucou'
echo    - Donner tous les droits à cet utilisateur sur la base de données
echo.
echo Si vous souhaitez utiliser d'autres identifiants, vous devrez modifier
echo le fichier 'chatbot_ia/settings.py' en conséquence.
echo.
pause

REM Exécuter les migrations Django
echo.
echo Exécution des migrations Django...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERREUR: Impossible d'exécuter les migrations.
    pause
    exit /b 1
)
echo Migrations exécutées avec succès.

REM Créer un superutilisateur
echo.
echo Création d'un superutilisateur...
echo Vous allez maintenant créer un compte administrateur pour accéder à l'interface d'administration.
python manage.py createsuperuser

REM Terminer l'installation
echo.
echo ===============================================================================
echo                     Installation terminée avec succès!
echo ===============================================================================
echo.
echo Pour démarrer le serveur de développement, exécutez:
echo python manage.py runserver
echo.
echo Accédez ensuite à http://127.0.0.1:8000/ dans votre navigateur.
echo.
pause 