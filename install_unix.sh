#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les en-têtes
print_header() {
    echo -e "\n${YELLOW}===============================================================================${NC}"
    echo -e "${YELLOW}                     $1${NC}"
    echo -e "${YELLOW}===============================================================================${NC}\n"
}

# Fonction pour afficher les erreurs
print_error() {
    echo -e "${RED}ERREUR: $1${NC}"
}

# Fonction pour afficher les succès
print_success() {
    echo -e "${GREEN}$1${NC}"
}

# Vérifier si Python est installé
check_python() {
    if command -v python3 &>/dev/null; then
        python_cmd="python3"
    elif command -v python &>/dev/null; then
        python_version=$(python --version 2>&1 | awk '{print $2}')
        if [[ $(echo "$python_version" | cut -d. -f1) -ge 3 ]]; then
            python_cmd="python"
        else
            print_error "Python 3 n'est pas installé ou n'est pas dans le PATH."
            echo "Veuillez installer Python 3.10 ou plus récent depuis https://www.python.org/downloads/"
            exit 1
        fi
    else
        print_error "Python 3 n'est pas installé ou n'est pas dans le PATH."
        echo "Veuillez installer Python 3.10 ou plus récent depuis https://www.python.org/downloads/"
        exit 1
    fi
}

# Début du script
print_header "Installation du Projet ChatBot IA (Unix/Mac)"

# Vérifier si Python est installé
check_python
echo "Utilisation de $python_cmd"

# Créer l'environnement virtuel
echo -e "\nCréation de l'environnement virtuel Python..."
if [ -d "venv" ]; then
    echo "L'environnement virtuel existe déjà."
else
    $python_cmd -m venv venv
    if [ $? -ne 0 ]; then
        print_error "Impossible de créer l'environnement virtuel."
        exit 1
    fi
    print_success "Environnement virtuel créé avec succès."
fi

# Activer l'environnement virtuel et installer les dépendances
echo -e "\nInstallation des dépendances..."
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "Impossible d'installer les dépendances."
    exit 1
fi
print_success "Dépendances installées avec succès."

# Configurer le fichier .env
echo -e "\nConfiguration du fichier .env..."
if [ -f ".env" ]; then
    echo "Le fichier .env existe déjà."
    read -p "Voulez-vous le modifier ? (o/n): " modify
    if [[ "$modify" != "o" && "$modify" != "O" ]]; then
        echo "Conservation du fichier .env existant."
    else
        read -p "Entrez votre clé API OpenAI: " api_key
        echo "OPENAI_API_KEY=$api_key" > .env
        print_success "Fichier .env mis à jour avec succès."
    fi
else
    read -p "Entrez votre clé API OpenAI: " api_key
    echo "OPENAI_API_KEY=$api_key" > .env
    print_success "Fichier .env créé avec succès."
fi

# Configuration de la base de données
echo -e "\nConfiguration de la base de données PostgreSQL..."
echo -e "\nPour configurer la base de données PostgreSQL, vous avez deux options:"
echo -e "\n1. Utiliser le script SQL fourni (recommandé)"
echo "   Exécutez la commande: sudo -u postgres psql -f database_setup.sql"
echo -e "\n2. Configuration manuelle"
echo "   - Créer une base de données nommée 'chatbot_db'"
echo "   - Créer un utilisateur PostgreSQL 'alex' avec mot de passe 'coucou'"
echo "   - Donner tous les droits à cet utilisateur sur la base de données"
echo -e "\nSi vous souhaitez utiliser d'autres identifiants, vous devrez modifier"
echo "le fichier 'chatbot_ia/settings.py' en conséquence."
echo -e "\nAppuyez sur Entrée une fois la base de données configurée..."
read

# Exécuter les migrations Django
echo -e "\nExécution des migrations Django..."
$python_cmd manage.py migrate
if [ $? -ne 0 ]; then
    print_error "Impossible d'exécuter les migrations."
    exit 1
fi
print_success "Migrations exécutées avec succès."

# Créer un superutilisateur
echo -e "\nCréation d'un superutilisateur..."
echo "Vous allez maintenant créer un compte administrateur pour accéder à l'interface d'administration."
$python_cmd manage.py createsuperuser

# Terminer l'installation
print_header "Installation terminée avec succès!"
echo "Pour démarrer le serveur de développement, exécutez:"
echo "$python_cmd manage.py runserver"
echo -e "\nAccédez ensuite à http://127.0.0.1:8000/ dans votre navigateur."
echo 