# README

## Introduction

Ce projet utilise **Ollama** avec **Mistral 7XB** et nécessite une clé **OpenAI** pour l'évaluation des prompts. L'objectif est d'installer et de configurer la base de données vectorielle pour **PG Vector** et **ChromaDB**, puis de lancer l'évaluation avec la commande `prompt eval`.

## Prérequis

1. **Ollama** avec **Mistral 7XB**.
2. Une clé **OpenAI**.
3. PostgreSQL avec **PG Vector** installé.
4. **ChromaDB** installé.

## Installation

### Étape 1: Cloner le dépôt

Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/votre-utilisateur/votre-repo.git
cd votre-repo
```

### Étape 2: Installer les dépendances

Installez les dépendances requises en utilisant `pip` :

```bash
pip install -r requirements.txt
```

### Étape 3: Configurer PostgreSQL avec PG Vector

Assurez-vous d'avoir PostgreSQL installé. Ensuite, suivez les étapes pour installer **PG Vector** :

1. Ajoutez l'extension PG Vector à votre base de données :

    ```sql
    CREATE EXTENSION IF NOT EXISTS vector;
    ```

2. Modifiez votre configuration de base de données pour utiliser PG Vector. Par exemple, ajoutez cette ligne dans votre fichier de configuration PostgreSQL (`postgresql.conf`) :

    ```plaintext
    shared_preload_libraries = 'pgvector'
    ```

### Étape 4: Configurer les variables d'environnement

Créez un fichier `.env` à la racine de votre projet et ajoutez-y votre clé **OpenAI** qui servira au scoring de promptfoo :

```env
OPENAI_API_KEY=your_openai_api_key
```

## Utilisation

Pour lancer l'évaluation des prompts, utilisez la commande suivante :

```bash
prompt eval
```

## Configuration

### Variables d'environnement

Assurez-vous que les variables d'environnement suivantes sont correctement définies dans votre fichier `.env` :

```env
OPENAI_API_KEY=your_openai_api_key
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
VECTOR_TABLE=your_vector_table_name
```

### Exemple de prompt

Pour évaluer un prompt avec **OpenAI**, utilisez la clé de l'API définie dans votre fichier `.env` et lancez la commande `prompt eval` :

```bash
prompt eval "foo"
```