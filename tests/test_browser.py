import time
import pytest
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from config.settings import BASE_DIR
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# Замените этот путь на путь к вашему исполняемому файлу chromedriver
DRIVER_PATH = 'D:\\webdriver\\chromedriver.exe'

@pytest.fixture
def root_url():
    return f'file:///{BASE_DIR / "store-template" / "index.html"}'




@pytest.fixture
def headless_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Включаем режим без графического интерфейса

    # Используем Service для указания пути к ChromeDriver
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    
    yield browser
    browser.quit()
    
    
def test_bs(browser: WebDriver, root_url: str):
    browser.get(root_url)
    browser.maximize_window()
    browser.find_element(By.ID, 'start-purchase-link').click()
    
    bs = BeautifulSoup(browser.page_source, 'html.parser')
    rows = bs.find_all('div', attrs={'class': 'card-body'})
    
    products = []
    for row in rows:
        title = row.find('h4').text
        products.append(title)
        
    with open('products.txt', 'w') as file:
        file.write('\n'.join(products))





def test_interactions(browser: WebDriver, root_url: str):
    browser.get(root_url)
    browser.maximize_window()
    browser.find_element(By.ID, 'navbarDropdown').click()
    
    browser.find_element(By.LINK_TEXT, 'Профиль').click()
    
    browser.find_element(By.LINK_TEXT, 'Оформить заказ').click()
    
    
    first_name = browser.find_element(By.ID, 'firstName')
    first_name.send_keys('John')
    time.sleep(2)
    
    last_name = browser.find_element(By.ID, 'lastName')
    last_name.send_keys('Doe')
    time.sleep(2)
    
    assert first_name.get_attribute('value') == 'John'
    assert last_name.get_attribute('value') == 'Doe'
    
    remember_data = browser.find_element(By.ID, 'rememberData')
    remember_data.click()
    time.sleep(2)
    assert remember_data.is_selected()
    
    remember_data.click()
    assert remember_data.is_selected() is False
    


def test_find_by_xpath_selectors(browser: WebDriver, root_url: str):
    browser.get(root_url)
    browser.maximize_window()
    browser.find_element(By.ID, 'start-purchase-link').click()
    time.sleep(2)
    
    el1 = browser.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div[4]/div/div[2]/button')
    
    browser.find_element(By.ID, 'navbarDropdown').click()
    
    el2 = browser.find_element(By.XPATH, '//*[@id="navbarResponsive"]/ul/li[3]/ul/li[1]/a')
    
    assert el1.text == 'Отправить в корзину'
    assert el2.text == 'Профиль'




def test_find_by_css_selectors(headless_chrome: WebDriver, root_url: str):
    headless_chrome.get(root_url)
    headless_chrome.maximize_window()
    
    # Ожидаем и кликаем по ссылке
    start_purchase_link = WebDriverWait(headless_chrome, 10).until(
        EC.element_to_be_clickable((By.ID, 'start-purchase-link'))
    )
    start_purchase_link.click()

    # Ожидаем появления элементов
    el1 = WebDriverWait(headless_chrome, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-disabled="true"]'))
    )
    el2 = WebDriverWait(headless_chrome, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#navbarDropdown'))
    )

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
    WebDriverWait(browser, timeout=5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="trash"]/i')))
    
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


def _switch_to_another_handler(browser, original_page_handler):
    for window_handle in browser.window_handles:
        if window_handle != original_page_handler:
            browser.switch_to.window(window_handle)
            break

def test_interaction_with_tabs_or_windows(browser: WebDriver, root_url: str):
    browser.get(root_url)
    browser.maximize_window()
    
    original_page_handler = browser.current_window_handle
    
    login_page_link = browser.find_element(By.LINK_TEXT, 'Войти')
    login_page_link.click()
    
    _switch_to_another_handler(browser, original_page_handler)
    
    # Используем browser.title для получения заголовка страницы
    login_title = browser.title
    assert login_title == 'Store - Авторизация', f"Expected 'Store - Авторизация', got '{login_title}'"
    
    browser.close()
    browser.switch_to.window(original_page_handler)
    
    catalog_page = browser.find_element(By.LINK_TEXT, 'Каталог')
    catalog_page.click()
    
    _switch_to_another_handler(browser, original_page_handler)
    
    # Используем browser.title для получения заголовка страницы
    catalog_title = browser.title
    assert catalog_title == 'Store - Каталог', f"Expected 'Store - Каталог', got '{catalog_title}'"

    browser.close()
    browser.switch_to.window(original_page_handler)
    
    # Используем browser.title для получения заголовка страницы
    main_title = browser.title
    assert main_title == 'Store', f"Expected 'Store', got '{main_title}'"
