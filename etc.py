import json
import psycopg2
from blog.settings import BASE_DIR


data = json.loads((open(BASE_DIR/'initial_data.json', 'r').read()))

connection = psycopg2.connect(
    database="blog_db",
    user="svetlanarudneva",
    password="cj,frfjhtk2003",
    host="localhost",
    port="5432"
)

cur = connection.cursor()

for i in range(len(data)):
    print(data[i])

print("database open successfully")
