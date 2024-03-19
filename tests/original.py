
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = 'D:\\webdriver\\chromedriver.exe'  # Обратите внимание на двойные обратные слэши

def test_browser():
    service = Service(executable_path=DRIVER_PATH)
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()
    browser.get("https://www.google.com")
    browser.quit()
'''


'''
This function tests the browser functionality using Selenium WebDriver.
It opens a Chrome browser, maximizes the window, navigates to Google's homepage,
and then closes the browser.
'''
    
    
    
import time
import pytest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # Add the missing import statement here
from config.settings import BASE_DIR


@pytest.fixture
def root_url():
    return f'file:///{BASE_DIR / "store-template" / "index.html"}'


DRIVER_PATH = Path('D:/webdriver/chromedriver.exe')  # Обратите внимание на двойные обратные слэши

def test_titles_are_correct(root_url):
    service = Service(executable_path=DRIVER_PATH)
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()
    
    time.sleep(2)
    browser.get(root_url)
    
    time.sleep(2)
    main_title = browser.find_element(By.CLASS_NAME, 'navbar-brand')
    assert main_title.text == 'Store'
    
    time.sleep(2)
    purchase_link = browser.find_element(By.ID, 'start-purchase-link')
    purchase_link.click()
    
    time.sleep(2)
    product_title = browser.find_element(By.ID, 'product-title')
    assert product_title.text == 'Store'
    
    time.sleep(2)
    browser.quit()

