# EFREI-2024-ADDE92-PROJET-BIGDATA-GROUP_5"

# Modelule: Application Of BigData - Projet

<image src="https://alexandrecastro.dev/wp-content/uploads/2021/12/azure-container-apps.jpg" width=800 center>

[![Downloads](https://static.pepy.tech/personalized-badge/azure?period=month&units=international_system&left_color=blue&right_color=black&left_text=azure)](https://pepy.tech/project/azure) [![Downloads](https://static.pepy.tech/personalized-badge/docker?period=month&units=international_system&left_color=blue&right_color=yellow&left_text=docker)](https://pepy.tech/project/docker)   [![Downloads](https://static.pepy.tech/personalized-badge/requests?period=month&units=international_system&left_color=brightgreen&right_color=orange&left_text=requests)](https://pepy.tech/project/requests) [![Downloads](https://static.pepy.tech/personalized-badge/iris?period=month&units=international_system&left_color=blue&right_color=green&left_text=iris)](https://pepy.tech/project/openweather) [![Downloads](https://static.pepy.tech/personalized-badge/github?period=month&units=international_system&left_color=black&right_color=orange&left_text=github)](https://pepy.tech/project/github) [![GitHub Actions](https://github.com/actions/toolkit/actions/workflows/main.yml/badge.svg)](https://github.com/actions/toolkit/actions/workflows/main.yml) [![Downloads](https://static.pepy.tech/personalized-badge/py?period=month&units=international_system&left_color=black&right_color=blue&left_text=Python)](https://pepy.tech/project/python)

> ## Objectifs

Déployer, à travers d'une API, un modèle entraîné de prédiction en utilisant la philosophie DevOps sur un fournisseur de services cloud.

> ## Prérequis
 - Python
 - Docker
 - Github
 - Azure Container Registry (ACR)
 - Azure Container Apps (ACA)

https://learn.microsoft.com/en-us/azure/developer/python/containers-in-azure-overview-python?tabs=vscode-ide

> NOTE: Ce projet a pour objectif de mettre à disposition dans un Container Apps, une API de prédiction de la classe des fleurs d'iris sur un fournisseur de srervice cloud. Dans notre cas, nous avons choisi Azure. Cet API doit être déployé sur le Azure Container Apps par un workflow Github Action.

> ## 1. Notre modèle de machine learning
Notre modèle machine learning consiste à utiliser `KNeighborsClassifier()` de la bibliothèque scikit learn pour pouvoir entrainer les données et la prédiction. Le modèle k-NN est utilisé avec l'ensemble de données Iris en raison de sa simplicité, de la distinctivité des classes et de son absence d'hypothèses sur la distribution des données.
Les données d'iris utilisé pour l'entrainement du modèle sont directement importer du site https://archive.ics.uci.edu/dataset/53/iris à l'aide de la commande "`iris = fetch_ucirepo(id=53)`". Ceci nous évite de télécharger le jeu de données en local.

> ## 2. Développement de l'API
Notre API, que vous pouvez retrouver dans le fichier `app.py`, est développé en Python et a nécessité l'utilisation des packages suivants:

    - Flask
    - Premoetheus client
    - Joblib
    - Numpy

Dans le fichier `app.py`, vous avez 3 routes:

 - `/`: Renvoyer la description de l'API
 - `/predict`: Renvoyer la prédiction de la classe des fleurs d'iris sur l'image les paramètres envoyée.
 - `/metrics`: Renvoyer le compte des prédictions de chaque classe des fleurs d'iris sur toutes les requêtes effectuées.

Les paramètres de notre API `https://base_url/predict` sont :

- `sl` : pour la Sepal Length
- `sw` : pour la Sepal Width
- `pl` : pour la Petal Length
- `pw` : pour la Petal Width

Pour les métriques, nous avon utilisé le package `prometheus_client` qui nous renvoie les totaux des reqêtes dans l'ensemble ainsi que le nombre de prédiction de chaque classe.

Notre application peut être déployé et testé en local. Et pour faciliter les tests, vous pouvez utiliser le fichier `test.py` en passant à la variable `BASE_URL` le lien de l'API. Ici c'est `http://127.0.0.1:80`.

> ## 3. Configuration du Dockerfile
    
docker build -t projectgroupe5 .

`projectgroupe5` : nom de l'image

`.` : répertoire contenant le fichier dockerfile

Si vous rencontrez des erreurs avec l'image docker:

1. Vérifier si Docker est en Cours d'Exécution

Ouvrez une nouvelle fenêtre de terminal.
Tapez docker info ou docker version. Si Docker est en cours d'exécution, ces commandes retourneront des informations sur Docker. Si elles échouent, cela confirme que Docker n'est pas en cours d'exécution.

2. Démarrer le Daemon Docker

Si vous utilisez Docker Desktop, ouvrez l'application Docker Desktop. Elle devrait démarrer le daemon Docker automatiquement.
Si vous utilisez Docker dans un environnement Linux, Vous pouvez le faire en exécutant la commande: sudo systemctl start docker

3. Relancer la commande : docker build -t projectgroupe5 .

> ## 4. Configuration d"un workflow Github Action
- Créer le fichier `.github/workflows/main.yml` dans le dossier du projet
- Ajouter le contenu suivant :
````
on: [push]
name: Linux_Container_Workflow

jobs:
    build-and-deploy:
        runs-on: ubuntu-latest
        env:
          PROJET_NAME: projectgroupe5
          CONTAINER_ENV: groupe5-newcontainer-env
          CONTAINER_APP: groupe5-newcontainer-app
          LOCATION: francecentral
        steps:
        # checkout the repo
        - name: 'Checkout GitHub Action'
          uses: actions/checkout@main
          
        - name: 'Login via Azure CLI'
          uses: azure/login@v1
          with:
            creds: ${{ secrets.AZURE_CREDENTIALS }}

        - uses: actions/checkout@v3
        - uses: hadolint/hadolint-action@v3.1.0
          with:
            dockerfile: Dockerfile
        
        - name: 'Build and push image'
          uses: azure/docker-login@v1
          with:
            login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
            username: ${{ secrets.REGISTRY_USERNAME }}
            password: ${{ secrets.REGISTRY_PASSWORD }}
        - run: |
            docker build . -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/${{ env.PROJET_NAME }}:${{ github.sha }}
            docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/${{ env.PROJET_NAME }}:${{ github.sha }}

        - name: Create Azure container environment
          run: |
            az containerapp env create -n ${{ env.CONTAINER_ENV }} -g  ${{ secrets.RESOURCE_GROUP }} --location ${{ env.LOCATION }}

        - name: Build and deploy Container App 
          uses: azure/container-apps-deploy-action@v1
          with:
            containerAppName: ${{ env.CONTAINER_APP }}
            containerAppEnvironment: ${{ env.CONTAINER_ENV }}
            imageToDeploy: ${{ secrets.REGISTRY_LOGIN_SERVER }}/${{ env.PROJET_NAME }}:${{ github.sha }}
            acrName: ${{ secrets.REGISTRY_USERNAME }}
            acrUsername: ${{ secrets.REGISTRY_USERNAME }}
            acrPassword: ${{ secrets.REGISTRY_PASSWORD }}
            resourceGroup: ${{ secrets.RESOURCE_GROUP }}
````

Cette configuration permet de:
- Se connecter avec Azure CLI
- Créer l'environnement Azure Container Environment
- Construire et pusher l'image docker dans l'Azure Container Apps

Outre les secrets défini en global pour le projet, nous avons redéfini des variables d'environnement pour les PROJET_NAME, CONTAINER_ENV, CONTAINER_APP et la LOCATION afin de maintenir le workflow Github Action plus facilement.

À la fin de la configuration, le workflow Github Action est disponible sur Github après push et biensûr paramétrage des `secrets` utilisés. Si les secrets ne sont pas paramétrés, vous aurez une erreur lors de l'appel de l'API. Mais dans le cadre de ce projet, les secrets sont déjà disponsibles dans le projet github.

Une fois le workflow Github Action exécuté avec succès, on peut aller dans Azure Container Apps pour voir notre image bien déployé. Nous pouvons dès à présent passer au test.

> ## 5. Test de l'API

Pour tester notre API, nous allons faire des tests en local (curl ou postman, c'est comme vous voulez) et des tests via le lien du Container Apps.

> ### 5.1 Test en local

- API d'information `http://127.0.0.1:80/`
```
curl "http://127.0.0.1:80/"
```
 Response:
```
{
  "Message": "Bonjour! Appelez l'api /predict avec les paramètres: sl (sepal lenght), sw (sepal width), pl (petal lenght), pw (petal width)."
}
```

- API de prédiction `http://127.0.0.1:80/predict`
```
curl "http://127.0.0.1:80/predict?pl=1&pw=5&sl=3&sw=4"
```
 Response:
```
{
    "prediction": "Iris-setosa"
}
```

- API des metrics `http://127.0.0.1:80/metrics`
```
curl "http://127.0.0.1:80/metrics"
```
 Response:
```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 188.0
python_gc_objects_collected_total{generation="1"} 289.0
python_gc_objects_collected_total{generation="2"} 28.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 220.0
python_gc_collections_total{generation="1"} 20.0
python_gc_collections_total{generation="2"} 1.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="10",patchlevel="12",version="3.10.12"} 1.0
# HELP api_calls_total Total number of API calls
# TYPE api_calls_total counter
api_calls_total 1.0
# HELP api_calls_created Total number of API calls
# TYPE api_calls_created gauge
api_calls_created 1.705753130637908e+09
# HELP api_setosa_predictions_total Total number of Iris Setosa predictions
# TYPE api_setosa_predictions_total counter
api_setosa_predictions_total{endpoint="/predict",predictions="Iris-setosa"} 1.0
# HELP api_setosa_predictions_created Total number of Iris Setosa predictions
# TYPE api_setosa_predictions_created gauge
api_setosa_predictions_created{endpoint="/predict",predictions="Iris-setosa"} 1.705753285250599e+09
# HELP api_virginica_predictions_total Total number of Iris Virginica predictions
# TYPE api_virginica_predictions_total counter
# HELP api_versicolor_predictions_total Total number of Iris Versicolor predictions
# TYPE api_versicolor_predictions_total counter
```

> ### 5.2 Test via le lien du Container Apps

Pour ce test, vous devez juste remplacer l'url de base par le celui du Container Apps. C'est à dire en lieu et place de `http://127.0.0.1:80`, utiliser `https://groupe5-newcontainer-app.politewater-20dc8a0f.francecentral.azurecontainerapps.io`.

### Autres

Vous pouvez aussi outrepasser le fait de faire le testmanuellement en saisissant à chaque fois les paramètres de l'API. utilisez donc le fichier `test.py` qui vous facilite les tests en générant aléatoirement les valeurs des paramètres entre 0 et 10, vous lance les requêtes et vous fournit les resultats ainsi que les métriques.

> Remarques

La principale défficulté rencontrée dans la réalisation de ce proejt est la configuration de l'Azure Container Apps. Il est aussi à notre que, si jamais vous décider de déployer l'API sur un autre port que le port 80, vous devez configurer ce port dans votre Container Apps ppour pouvoir y avoir accès si vous ne pourrez pas l'utiliser via le lien du container.


> ###################################################
- AGBONON EDAGBEDJI Yao Anicet
- SIAKE TCHOUAMOU Sophie Manuella
- BOUDOUKHA Maroua
- AGBAHOLOU Marie-Lynne Murielle Essénahoun
- GUZMAN Kymsy
- WANDJI K Fréderique
> ###################################################
