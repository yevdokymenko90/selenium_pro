from selenium import webdriver
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = 'D:\\webdriver\\chromedriver.exe'  # Обратите внимание на двойные обратные слэши

def test_browser():
    service = Service(executable_path=DRIVER_PATH)
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()
    browser.get("https://www.google.com")
    browser.quit()


    """
    This function tests the browser functionality using Selenium WebDriver.
    It opens a Chrome browser, maximizes the window, navigates to Google's homepage,
    and then closes the browser.
    """
    
    