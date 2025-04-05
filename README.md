# Projet_Adv_Git
Ce projet a pour but de suivre en temps réel le prix de l’argent dollars US en le scrappant automatiquement depuis un site web, puis en l’affichant via un tableau de bord interactif développé avec Dash.

## Fonctionnement général :
- Scraping toutes les 5 minutes du site avec les prix de l'argent
- Enregistrement des données (timestamp + prix) dans un fichier CSV
- Affichage des données sur un dashboard web
- Génération d’un rapport quotidien à 20h avec :
  - Prix d’ouverture et de clôture
  - Évolution (valeur et pourcentage)
  - Volatilité de la journée
  - Prix moyen
