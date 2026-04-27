# Full Auth Flask API

## Description
A secure Flask backend implementing JWT authentication and user-owned resources (Notes).  
Supports full CRUD operations, pagination, and access control so users cannot view or edit each other’s data.  
Designed to integrate with the provided frontend productivity apps.

## Installation
```bash
# Clone the repo
git clone <your-repo-url>
cd Full-Auth-Flask-API

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
flask db upgrade

# Seed the database with demo data
python seed.py


# 
python3 app.py
or
flask run
