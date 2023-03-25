import json
import psycopg2
from blog.settings import BASE_DIR


# data = json.loads((open(BASE_DIR/'initial_data.json', 'r').read()))

connection = psycopg2.connect(
    database="blog",
    user="postgres",
    password="postgres",
    host="postgres",
    port="5432"
)

cur = connection.cursor()

# for i in range(len(data)):
#     print(data[i])

print("database open successfully")
