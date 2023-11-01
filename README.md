# Interface pour controle_codage_pmsi

Interface sous forme d'application web pour l'outil [controle_codage_pmsi](https://github.com/curie-data-factory/consore-services/blob/main/consore_services%2Fcontrole_codage_pmsi%2FREADME.md) du dépot [consore-services](https://github.com/curie-data-factory/consore-services).

## Prérequis

- Python>=3.9
- Python libs (requirements.txt)
- Docker (si lancement via Docker)

## Installation

Dans un dossier de travail `WORKDIR`:

- cloner le dépot [consore-services](https://github.com/curie-data-factory/consore-services)
    - Suivre les indication d'installation (pas nécessaire pour Docker)
- cloner ce dépot
    - Installer les librairies python (requirements.txt) dans l'environnement virtuel créé lors de l'installation de `consore-services (pas nécessaire pour Docker)

### Configuration

- Copier le fichier `template_config.yaml` en `config.yaml`
- Modifier à minima les `usernames` et la `key`
- Plus d'informations [ici](https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/)

### Lancer localement

```
streamlit run app.py
```

Visualiser l'interface à l'url http://localhost:8501

### Lancer via Docker

#### Compiler l'image

Se placer dans le dossier de travail `WORKDIR`

```
docker build -f controle_codage_pmsi_ui/Dockerfile -t controle_codage_pmsi_ui .
```

**ATTENTION:** l'image compilée copie le dossier [consore-services](https://github.com/curie-data-factory/consore-services) entièrement dans l'image excepté les fichiers indiqués dans le `.dockerginore`. Si d'autres fichiers avec des données sensibles sont présents dans le dossier, les rajouter au fichier `.dockerignore` pour ne pas les copier dans l'image.

#### Lancer le container

```
docker run --name controle_codage_pmsi_ui -d -v $PWD/config.yaml:/app/config.yaml -v $PWD/data/config.json:/app/data/config.json -p 8501:8501 controle_codage_pmsi_ui
```

## Utilisation de l'interface

L'interface devrait être assez simple et intuitive pour ne pas nécessiter d'explication. Elle permet de lancer l'outil `controle_codage_pmsi` dont le fonctionnement est exliqué [ici](https://github.com/curie-data-factory/consore-services/blob/main/consore_services%2Fcontrole_codage_pmsi%2FREADME.md)

### Données

Un fichier keywords.xlsx comme décrit dans la [documentation de l'outil](https://github.com/curie-data-factory/consore-services/blob/main/consore_services%2Fcontrole_codage_pmsi%2FREADME.md#fichiers-dentr%C3%A9e) doit être fourni.
A défaut, le fichier de test est téléchargeable via l'interface pour servir de modèle.
