import pytest
from selenium import webdriver as wd
import time

driver_path = '../webdriver/chromedriver'
@pytest.fixture()
def test_setup():
    global wd
    wd = wd.Chrome(driver_path) 
    wd.maximize_window()
    wd.get('https://www.bestbuy.com/site/pny-geforce-gt1030-2gb-pci-e-3-0-graphics-card-black/5901353.p?skuId=5901353')
    time.sleep(3)

def test_place_order(test_setup):
    
    try:
        add_to_cart_button = wd.find_element_by_class_name('btn-disabled')
        add_to_cart_button.click()
        time.sleep(3)


    except:
        add_to_cart_button = wd.find_element_by_class_name('btn-primary')
        add_to_cart_button.click()
        time.sleep(3)