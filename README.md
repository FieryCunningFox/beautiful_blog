# beautiful_blog
#blog with django, CSS, HTML and JavaScript, postgresql as Database
#there is also parser news from FOXNEWS

#to connect db:
  $brew link postgresql --force
  $brew services start postgresql
  $pg_ctl -D blog_db -l logfile start

#to create db:
  $createdb blog_db
  $init blog_db

#to start:
  $pip install -r requirements.txt
  $python manage.py runserver
  
#to start docker-container:
  $sudo docker build -t dmosk/nginx:v1 . - in Dockerfile directory

#to parse news:
  $python3 parser_news.py



$virtualenv blog_env

<img width="1494" alt="image" src="https://user-images.githubusercontent.com/91421235/170865508-68f1c6af-61e0-4b15-b841-3634a53e74e7.png">

<img width="1509" alt="image" src="https://user-images.githubusercontent.com/91421235/170865526-8e2c0123-cd83-4438-ac77-fa6069d07261.png">

<img width="1510" alt="image" src="https://user-images.githubusercontent.com/91421235/170865546-2b765c03-637f-4b73-b5bf-c841c81840be.png">

<img width="1498" alt="image" src="https://user-images.githubusercontent.com/91421235/170865564-a44c07db-18a4-4ad3-b653-1608f7a273d4.png">
