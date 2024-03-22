from selenium import webdriver
import webdriver_manager
import json
import pytest
from config.settings import BASE_DIR

def get_config_file_path():
    return BASE_DIR / 'config' / 'test_config.json'

@pytest.fixture
def config(scope='session'):
    with open(get_config_file_path()) as config_file:
        config = json.load(config_file)
    return config


def set_option(opts, config):
   if config['mode'] == 'headless':
       opts.add_argument('--headless')
 

@pytest.fixture       
def browser(config):
    if config['browser'] == 'Chrome':
        opts = webdriver.ChromeOptions()
        set_option(opts, config)
        driver = webdriver.Chrome(options=opts)
    elif config['browser'] == 'Firefox':
        opts = webdriver.FirefoxOptions()
        set_option(opts, config)
        driver = webdriver.Firefox(options=opts)
    else:
        raise Exception('Unsupported browser')
    
    yield driver
    
    driver.quit()
    