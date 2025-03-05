#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script d'installation pour le projet ChatBot IA.
Ce script aide à configurer l'environnement de développement.
"""

import os
import sys
import subprocess
import platform
import getpass

def print_header(message):
    """Affiche un message d'en-tête formaté."""
    print("\n" + "=" * 80)
    print(f" {message} ".center(80, "="))
    print("=" * 80 + "\n")

def run_command(command, error_message="Une erreur s'est produite"):
    """Exécute une commande shell et gère les erreurs."""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"ERREUR: {error_message}")
        return False

def create_virtual_env():
    """Crée et active un environnement virtuel Python."""
    print_header("Création de l'environnement virtuel Python")
    
    if os.path.exists("venv"):
        print("L'environnement virtuel existe déjà.")
        return True
    
    if platform.system() == "Windows":
        success = run_command("python -m venv venv", 
                             "Impossible de créer l'environnement virtuel")
        if success:
            print("Environnement virtuel créé avec succès.")
            print("Pour l'activer, exécutez: venv\\Scripts\\activate")
    else:
        success = run_command("python3 -m venv venv", 
                             "Impossible de créer l'environnement virtuel")
        if success:
            print("Environnement virtuel créé avec succès.")
            print("Pour l'activer, exécutez: source venv/bin/activate")
    
    return success

def install_dependencies():
    """Installe les dépendances du projet."""
    print_header("Installation des dépendances")
    
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", 
                      "Impossible d'installer les dépendances")

def create_env_file():
    """Crée le fichier .env avec la clé API OpenAI."""
    print_header("Configuration du fichier .env")
    
    if os.path.exists(".env"):
        print("Le fichier .env existe déjà.")
        modify = input("Voulez-vous le modifier ? (o/n): ").lower() == 'o'
        if not modify:
            return True
    
    api_key = getpass.getpass("Entrez votre clé API OpenAI: ")
    
    try:
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("Fichier .env créé avec succès.")
        return True
    except Exception as e:
        print(f"ERREUR: Impossible de créer le fichier .env: {str(e)}")
        return False

def setup_database():
    """Configure la base de données PostgreSQL."""
    print_header("Configuration de la base de données")
    
    print("Pour configurer la base de données PostgreSQL, vous devez:")
    print("1. Créer une base de données nommée 'chatbot_db'")
    print("2. Créer un utilisateur PostgreSQL avec les informations suivantes:")
    print("   - Nom d'utilisateur: alex")
    print("   - Mot de passe: coucou")
    print("   - Droits: Tous les droits sur la base de données 'chatbot_db'")
    print("\nSi vous souhaitez utiliser d'autres identifiants, vous devrez modifier")
    print("le fichier 'chatbot_ia/settings.py' en conséquence.")
    
    input("\nAppuyez sur Entrée une fois la base de données configurée...")
    return True

def run_migrations():
    """Exécute les migrations Django."""
    print_header("Exécution des migrations Django")
    
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} manage.py migrate", 
                      "Impossible d'exécuter les migrations")

def create_superuser():
    """Crée un superutilisateur Django."""
    print_header("Création d'un superutilisateur")
    
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    print("Vous allez maintenant créer un compte administrateur pour accéder à l'interface d'administration.")
    return run_command(f"{python_cmd} manage.py createsuperuser", 
                      "Impossible de créer le superutilisateur")

def main():
    """Fonction principale du script d'installation."""
    print_header("Installation du Projet ChatBot IA")
    
    steps = [
        ("Création de l'environnement virtuel", create_virtual_env),
        ("Installation des dépendances", install_dependencies),
        ("Configuration du fichier .env", create_env_file),
        ("Configuration de la base de données", setup_database),
        ("Exécution des migrations", run_migrations),
        ("Création d'un superutilisateur", create_superuser)
    ]
    
    for step_name, step_func in steps:
        print(f"\n>> Étape: {step_name}")
        success = step_func()
        if not success:
            print(f"\nL'étape '{step_name}' a échoué. Installation interrompue.")
            sys.exit(1)
    
    print_header("Installation terminée avec succès!")
    print("Pour démarrer le serveur de développement, exécutez:")
    
    if platform.system() == "Windows":
        print("venv\\Scripts\\python manage.py runserver")
    else:
        print("venv/bin/python manage.py runserver")
    
    print("\nAccédez ensuite à http://127.0.0.1:8000/ dans votre navigateur.")

if __name__ == "__main__":
    main() 