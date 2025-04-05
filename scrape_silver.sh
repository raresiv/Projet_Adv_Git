#!/bin/bash

# URL de la page avec le prix de l'argent
URL="https://tradingeconomics.com/commodity/silver"

# Récupère le contenu HTML de la page
HTML=$(curl -s "$URL")

# Extrait le prix de l'argent
SILVER_PRICE=$(echo "$HTML" | grep -oP '(?<="value":)[0-9.]+' | head -1)

# Date et heure actuelles
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Pour enregistrer les données
OUTPUT_FILE="/home/ubuntu/dash-dashboard/silver_prices.csv"

# SI le fichier n'existe pas on le crée avec une ligne d'en tête
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Timestamp,Price" > "$OUTPUT_FILE"
fi

# Ajout de la ligen avec les données actuelles dans le fichier
echo "$TIMESTAMP,$SILVER_PRICE" >> "$OUTPUT_FILE"

echo "Scraped Silver Price: $SILVER_PRICE USD (Saved to $OUTPUT_FILE)"
