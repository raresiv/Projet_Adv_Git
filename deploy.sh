#!/bin/bash
#!/bin/bash

echo "Starting deployment process..."

# vérifie si cron est installé sinon on l'installe
if ! command -v cron &> /dev/null; then
    echo "Cron is not installed. Installing..."
    sudo apt update && sudo apt install cron -y
fi

# Vérifie si cron est en cours d'éxécution sinon on le démarre
if ! pgrep cron > /dev/null; then
    echo "Cron is not running. Starting..."
    sudo systemctl enable cron
    sudo systemctl start cron
fi

echo "Cron service verified!"

# Tâche de scraping toutes les 5min si elle existe ps déjà
SCRAPING_JOB="*/5 * * * * /home/ubuntu/dash-dashboard/scrape_silver.sh"

(crontab -l 2>/dev/null | grep -qF "$SCRAPING_JOB") || (echo "$SCRAPING_JOB" | crontab -)

echo "Data scraping cron job verified!"

# Ajoute la tâche quotidienne de génération du rapport à 20h si elle n'existe pas
REPORT_JOB="0 20 * * * /home/ubuntu/venv/bin/python /home/ubuntu/dash-dashboard/generate_report.py >> /home/ubuntu/report_log.txt 2>&1"

(crontab -l 2>/dev/null | grep -qF "$REPORT_JOB") || (crontab -l 2>/dev/null; echo "$REPORT_JOB") | crontab -

echo "Daily report cron job verified!"

# MAJ des fichiers du projet
cd ~/dash-dashboard
git pull origin main

source ~/venv/bin/activate

sudo systemctl restart dash_app

echo "Deployment complete!"
