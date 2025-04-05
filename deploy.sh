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


# ✅ 3.2 Ensure the daily report generation job is in crontab
REPORT_JOB="0 20 * * * /home/ubuntu/venv/bin/python /home/ubuntu/dash-dashboard/generate_report.py >> /home/ubuntu/report_log.txt 2>&1"

(crontab -l 2>/dev/null | grep -qF "$REPORT_JOB") || (crontab -l 2>/dev/null; echo "$REPORT_JOB") | crontab -

echo "Daily report cron job verified!"


# ✅ 4. Manual deployment (Only when script is manually executed)

cd ~/dash-dashboard
git pull origin main

source ~/venv/bin/activate

sudo systemctl restart dash_app

echo "Deployment complete!"
