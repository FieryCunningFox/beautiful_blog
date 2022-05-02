import requests
from pathlib import Path
import psycopg2
from psycopg2 import sql
import sqlite3
import time
import string
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from django.utils.text import slugify


BASE_DIR = Path(__file__).resolve().parent.parent
# CONN = psycopg2.connect(
#     database="blog_db",
#     user="svetlanarudneva",
#     password="cj,frfjhtk2003",
#     host="localhost",
#     port="5432"
# )
CONN = sqlite3.connect('db.sqlite3')

COLUMNS = ("title", "summary", "content", "image", "slug", "published_at", "link")

CURSOR = CONN.cursor()
QUERY = """SELECT * FROM home_newsmodel"""
CURSOR.execute(QUERY)


def generate_random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))


def generate_slug(text):
    new_slug = slugify(text)
    generate_slug(text + generate_random_string(5))
    return new_slug


def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def parse_news():
    browser = get_browser()
    link = "https://www.foxnews.com/"
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    blocks = soup.select(
        ".collection.collection-article-list .content.article-list .article")
    soup_urls = BeautifulSoup(str(blocks), features="html.parser")
    project_href = [i['href']
        for i in soup_urls.find_all('a', href=True) if i['href'] != "#"]
    project_href = list(set(project_href))
    return run_process(browser, project_href)


def run_process(browser, links):
    output_list_articles = []
    number_articles = 0
    for link_article in links:
        if connect_to_site(browser, link_article):
            # time.sleep(2)
            # html = browser.page_source
            html = requests.get(link_article)
            output_article = parse_html_article(html.text, link_article, number_articles)
            print(output_article)
            if output_article is not None:
                number_articles += 1
                output_list_articles.append(output_article)
        if number_articles >= 10:
            break
    return output_list_articles


def parse_html_article(html, link_article, number_articles):
    soup_article = BeautifulSoup(html, "html.parser")
    errors = 0
    title = ""
    summary = " "
    time_published = ""
    if title := soup_article.find("h1"):
        title = str(title.text)
    try:
        summary = soup_article.find("h2", class_="sub-headline")
        summary = str(summary.text)
    except Exception as e:
        # print(e)
        errors += 1
    try:
        time_published = soup_article.find("div", class_="article-date")
        time_published = time_published.text
    except Exception as e:
        # print(e)
        errors += 1
    try:
        if content := soup_article.find_all("p", class_="speakable"):
            article = '\n'.join(map(str, content))
        else:
            return None
    except Exception as e:
        # print(e)
        errors += 1
    if errors == 0:
        slug = "-".join(map(str, title.split()))[:70]
    return (title, summary, article, None, slug, time_published, link_article) if errors == 0 else None


def connect_to_site(browser, link_article):
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(link_article)
            WebDriverWait(browser, 6).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            return True
        except Exception as e:
            # print(e)
            connection_attempts += 1
            print(
                f"Error connecting to {link_article}. #Attempt {connection_attempts}")
    return False


if __name__ == "__main__":
    articles = parse_news()
    
    # insert = sql.SQL('INSERT INTO home_newsmodel("title", "summary", "content", "image", "slug", "published_at", "link") VALUES (%s, %s, %s, %s, %s, %s, %s)')
    CURSOR.executemany("""INSERT INTO home_newsmodel(title, summary, content, image, slug, published_at, link) VALUES (?, ?, ?, ?, ?, ?, ?)""", articles)    # CURSOR.executemany(insert, articles)
    
    # for i in range(len(articles)):
    #     CURSOR.execute("""INSERT INTO home_newsmodel(title, summary, content, image, slug, published_at, link) VALUES {}""".format(articles[i],))
    CONN.commit()
