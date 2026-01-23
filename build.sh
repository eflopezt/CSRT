#!/usr/bin/env bash
# exit on error
set -o errexit

# Force clean build
echo "==> Starting build process"

pip install --upgrade pip
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Collect static files
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createcachetable
python manage.py create_initial_superuser
