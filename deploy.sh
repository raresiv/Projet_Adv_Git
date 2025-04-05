#!/bin/bash
#!/bin/bash

echo "Starting deployment process..."

# On vérifie si cron est installé
if ! command -v cron &> /dev/null; then
    echo "Cron is not installed. Installing..."
    sudo apt update && sudo apt install cron -y
fi

# On vérifie s'il est actif ou non    
if ! pgrep cron > /dev/null; then
    echo "Cron is not running. Starting..."
    sudo systemctl enable cron
    sudo systemctl start cron
fi

echo "Cron service verified!"

# Tache pour scrapper toutes les 5min si c'est pas déjà fait avec crontab 
SCRAPING_JOB="*/5 * * * * /home/ubuntu/dash-dashboard/scrape_silver.sh"

# on vérifie la présence de la tâche dans le crontab sinon on l'ajoute
(crontab -l 2>/dev/null | grep -qF "$SCRAPING_JOB") || (echo "$SCRAPING_JOB" | crontab -)

echo "Data scraping cron job verified!"

cd ~/dash-dashboard
git pull origin main

source ~/venv/bin/activate

sudo systemctl restart dash_app

echo "Deployment complete!"
