#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_initial_superuser
