#!/bin/bash

# Navigate to project folder
cd ~/dash-dashboard

# Pull latest changes
git pull origin main

# Activate virtual environment
source ~/venv/bin/activate

# Restart Dash app using systemd
sudo systemctl restart dash_app

echo "Deployment complete!"
