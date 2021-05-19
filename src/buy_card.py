'''
Add to cart button HTML - DISABLED
<button 
    class="btn btn-disabled btn-lg btn-block add-to-cart-button" 
    disabled 
    type="button" 
    data-sku-id="6429442" 
    style="padding:0 8px">
        Sold Out
</button>

Can either purchase by:
    CSS selector 'add-to-cart-button'
    Class name   'btn-primary'
    Class name   'btn-disabled'
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import os
from dotenv import load_dotenv
from links import card_link
import time

load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

def get_input(args):
    brand, series = '', ''
    if len(args) < 3:
        return ('fitbit', 'test')
    elif len(args != 3):
        return ('nvidia', '3060ti')
    else:
        brand, series = args[1].lower(), args[2].lower()
    
    if series not in card_link:
        series = '3060ti'
    if brand not in card_link[series]:
        brand = 'nvidia'

    return brand, series

##########################
#####      MAIN      #####
##########################
'''
1. Get Best Buy web link to buy card
2. Login to Best Buy
3. Refresh every 2 seconds until 'Add to Cart button is clickable'
4. Wait until the 'How its going to work' message goes away and the button is clickable again
5. Click add to Cart
6. Go to Cart
7. Click Checkout
8. Manually finish this step.
'''
if __name__ == "__main__":

    brand, series = get_input(sys.argv)
    link = card_link[series][brand]
    driver = webdriver.Chrome('../webdriver/chromedriver')
    driver.get(link)
    driver.maximize_window()
    time.sleep(5)

    driver2 = webdriver.Chrome('../webdriver/chromedriver')
    driver2.get(link)

    while True:

        try:
            add_to_cart_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
            )
        except:
            driver.refresh()
            continue
        
        add_to_cart_button.click()
        print('clicked add to cart x1')
        time.sleep(10)

        driver.get("https://www.bestbuy.com/cart")
        print('navigated to cart')

        checkoutBtn = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[2]/div[1]/div/div/span/div/div[2]/div[1]/section[2]/div/div/div[3]/div/div[1]/button"))
        )
        checkoutBtn.click()
        print("clicked check out")
