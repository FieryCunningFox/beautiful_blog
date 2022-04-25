import requests
from pathlib import Path
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
    soup_urls = BeautifulSoup(str(blocks), features="lxml")
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
            output_article = parse_html_article(html.text)
            print(output_article)
            if output_article is not None:
                number_articles += 1
                output_list_articles.append(output_article)
        if number_articles >= 1:
            break
    return output_list_articles


def parse_html_article(html):
    soup_article = BeautifulSoup(html, "html.parser")
    errors = 0
    title = ""
    summary = " "
    time_published = ""
    if title := soup_article.find("h1"):
        title = title.text
    try:
        summary = soup_article.find("h2", class_="sub-headline")
        summary = summary.text
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
            article = str(content[0])
        else:
            return None
    except Exception as e:
        # print(e)
        errors += 1
    if errors == 0:
        slug = "-".join(map(str, title.split()))
        id = len(slug)
    return (id, title, summary, None, slug, time_published, article) if errors == 0 else None
    # return {'id': id, 'title': title, 'summary': summary, 'image': None, 'slug': slug, 'time_published': time_published, 'content': article} if errors == 0 else None


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
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    
    cursor.executemany("""INSERT INTO home_newsmodel
                   VALUES (?, ?, ?, ?, ?, ?, ?)""", articles)
    conn.commit()
# number = len(articles)
# if articles is not None:
#     for article in articles:
#         new_news = NewsModel()
#         new_news.title = article['title']
#         new_news.summary = article['summary']
#         new_news.published_at = article['time_published']
#         new_news.content = article['content']
#         new_news.save()
        
#     posts = (
#         NewsModel.objects.filter(published_at__lte=timezone.now())
#     )
# else:
#     number = 0
#     posts = []  