source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations SchoolEngine
python3 manage.py migrate
sqlite3 db.sqlite3 < seed.sql
python3 manage.py runserver