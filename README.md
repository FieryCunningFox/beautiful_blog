# beautiful_blog
blog with django, CSS, HTML and JavaScript
there is also parser news from FOXNEWS

to connect db:
  $ brew link postgresql --force
  $ brew services start postgresql
  $ pg_ctl -D blog_db -l logfile start

to create db:
  $ createdb blog_db
  $ init blog_db

to start:
  $pip install -r requirements.txt
  $python manage.py runserver
  
  
to parse news:
  $python parser_news.py



$ virtualenv blog_en
