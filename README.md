# EFREI-2024-ADDE92-PROJET-BIGDATA-GROUP_5-SIAKE__AGBONON__AGBAHOLOU__GUZMAN__BOUDOUKHA__WANDJI"

# Membres du groupe 5 :
- SIAKE TCHOUAMOU Sophie Manuella
- AGBONON EDAGBEDJI Yao Anicet
- AGBAHOLOU Marie-Lynne Murielle Essénahoun
- GUZMAN Kymsy
- BOUDOUKHA Maroua
- WANDJI K Fréderique

# Étapes de réalisation

## Choix Techniques:
- Flask : Utiliser pour créer l'API
- 

## Commandes Utilisés:
- 
- 

## Test de Charge:
- 

## Observations:
- 
- 

## Difficultés Rencontrées:
- 
- 


Construction de l'image Docker: 
docker build -t irisapi:v1 .

irisapi: nom de l'image
v1 : version de l'image (peut être modifié)
. : répertoire contenant le fichier dockerfile

Si vou rencontrez des erreurs avec l'image docker:
1. Vérifier si Docker est en Cours d'Exécution
Ouvrez une nouvelle fenêtre de terminal.
Tapez docker info ou docker version. Si Docker est en cours d'exécution, ces commandes retourneront des informations sur Docker. Si elles échouent, cela confirme que Docker n'est pas en cours d'exécution.
2. Démarrer le Daemon Docker
Si vous utilisez Docker Desktop, ouvrez l'application Docker Desktop. Elle devrait démarrer le daemon Docker automatiquement.
Si vous utilisez Docker dans un environnement Linux, Vous pouvez le faire en exécutant la commande: sudo systemctl start docker
3. Relancer la commande : docker build -t irisapi:v1 .