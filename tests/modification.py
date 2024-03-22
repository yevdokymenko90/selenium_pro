import time
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from config.settings import BASE_DIR
from selenium.common.exceptions import NoSuchElementException

# Замените этот путь на путь к вашему исполняемому файлу chromedriver
DRIVER_PATH = 'D:\\webdriver\\chromedriver.exe'

@pytest.fixture(scope="function")
def root_url():
    return f'file:///{BASE_DIR / "store-template" / "index.html"}'

def test_find_by_ccs_selectors(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()
    browser.find_element(By.ID, 'start-purchase-link').click()
    time.sleep(2)
    
    el1 = browser.find_element(By.CSS_SELECTOR, 'a[aria-disabled="true"]')
    el2 = browser.find_element(By.CSS_SELECTOR, '#navbarDropdown')
    
    el_list = [el1, el2]
    
    assert all(el is not None for el in el_list)
   


@pytest.fixture(scope="function")
def browser():
    # Указываем путь к chromedriver напрямую через Service
    browser_service = Service(executable_path=DRIVER_PATH)
    browser = webdriver.Chrome(service=browser_service)
    browser.maximize_window()
    yield browser
    browser.quit()


def test_add_to_cart_and_remove(browser: WebDriver, root_url: str):
    browser.get(root_url)
    browser.maximize_window()
    
    browser.find_element(By.ID, 'start-purchase-link').click()
    
    card_title = browser.find_element(By.CLASS_NAME, 'card-title').text
    
    card_footer = browser.find_element(By.CLASS_NAME, 'card-footer')
    card_footer.find_element(By.TAG_NAME, 'button').click()

    browser.find_element(By.ID, 'navbarDropdown').click()
    browser.find_element(By.LINK_TEXT, 'Профиль').click()

    added_item_title = browser.find_element(By.CLASS_NAME, 'card-title').text

    assert card_title == added_item_title
    time.sleep(2)
    try:
        browser.find_element(By.ID, 'trash').click()
    except NoSuchElementException:
        pass
    time.sleep(2)
    message = browser.find_element(By.TAG_NAME, 'h3').text
    assert message == 'Нет добавленных товаров'


def test_titles_are_correct(browser: WebDriver, root_url: str):
    browser.get(root_url)
    time.sleep(2)
    
    main_title = browser.find_element(By.CLASS_NAME, 'navbar-brand')
    assert main_title.text == 'Store', "Main title does not match expected"
    
    purchase_link = browser.find_element(By.ID, 'start-purchase-link')
    purchase_link.click()
    time.sleep(2)
    
    product_title = browser.find_element(By.ID, 'product-title')
    assert product_title.text == 'Store', "Product title does not match expected"
    
    