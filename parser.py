from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def stepik_parser():
    url = "https://stepik.org/catalog"

    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        products = soup.find_all('a', class_='course-card__title')
        course_title = [f'{i + 1}. {product.text.strip()}' for i, product in enumerate(products)]
        return course_title
    finally:
        browser.quit()
