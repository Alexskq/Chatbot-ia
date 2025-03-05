-- Script de configuration de la base de données PostgreSQL pour le projet ChatBot IA
-- Exécutez ce script avec les droits d'administrateur PostgreSQL

-- Création de l'utilisateur
CREATE USER alex WITH PASSWORD 'coucou';

-- Création de la base de données
CREATE DATABASE chatbot_db WITH OWNER = alex;

-- Attribution des privilèges
GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO alex;

-- Connexion à la base de données
\c chatbot_db

-- Attribution des privilèges sur le schéma public
GRANT ALL ON SCHEMA public TO alex;

-- Message de confirmation
\echo 'Configuration de la base de données terminée avec succès!'
\echo 'Base de données: chatbot_db'
\echo 'Utilisateur: alex'
\echo 'Mot de passe: coucou' 