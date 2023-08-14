from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


#I've redesigned the parser itself, I'm using selenium to get JS data and further work with HTML.
def stepik_parser():
    url = "https://stepik.org/catalog"

    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        
        #Also removed the regex and did a simple tag and class search, because now I can get the data normally.
        products = soup.find_all('a', class_='course-card__title')
        course_title = [f'{i + 1}. {product.text.strip()}' for i, product in enumerate(products)]
        return course_title
    finally:
        browser.quit()
