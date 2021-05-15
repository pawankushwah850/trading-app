command rm -f db.sqlite3
command cd user && rm -r migrations
command cd ../
command cd investment && rm -r migrations
command cd ../
command python manage.py makemigrations user
command python manage.py makemigrations investment
command python manage.py migrate
