import time
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config.settings import BASE_DIR
from webdriver_manager.chrome import ChromeDriverManager  # Импортировано для автоматического управления драйвером

@pytest.fixture(scope="function")
def root_url():
    return f'file:///{BASE_DIR / "store-template" / "index.html"}'

@pytest.fixture(scope="function")
def browser():
    # Создаем экземпляр веб-драйвера с автоматически подобранной версией chromedriver
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.maximize_window()
    yield browser
    browser.quit()

def test_titles_are_correct(browser, root_url):
    browser.get(root_url)
    time.sleep(2)
    
    main_title = browser.find_element(By.CLASS_NAME, 'navbar-brand')
    assert main_title.text == 'Store', "Main title does not match expected"
    
    purchase_link = browser.find_element(By.ID, 'start-purchase-link')
    purchase_link.click()
    time.sleep(2)
    
    product_title = browser.find_element(By.ID, 'product-title')
    assert product_title.text == 'Store', "Product title does not match expected"
