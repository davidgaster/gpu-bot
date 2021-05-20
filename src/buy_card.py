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
SECONDARY_USER = os.getenv('SECONDARY_USER')
PASSWORD = os.getenv('PASSWORD')
SECONDARY_PW = os.getenv('SECONDARY_PW')
CVV = os.getenv('CVV')

def get_input(args):
    brand, series = '', ''
    if len(args) < 3:
        return ('fitbit', 'test', '1')
    elif len(args) != 4:
        return ('nvidia', '3060ti', '1')
    else:
        brand, series, user = args[1].lower(), args[2].lower(), args[3]
    
    if series not in card_link:
        series = '3060ti'
    if brand not in card_link[series]:
        brand = 'nvidia'
    if user not in ['1', '2']:
        user = '1'

    return brand, series, user

def signin(driver, username, password):
    driver.get('https://www.bestbuy.com/identity/global/signin')
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'fld-e'))
        )
        email_field.send_keys(username)
    except:
        print('entering email failed after 10s')
    
    try:
        pw_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'fld-p1'))
        )
        pw_field.send_keys(password)
    except:
        print('entering password failed after 10s')

    try:
        signin_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.cia-form__controls__submit'))
        )
        signin_button.click()
        print("Clicked Sign in")
    except:
        print('Failed to locate sign in submission after 10s.')

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
if __name__ == '__main__':

    brand, series, user = get_input(sys.argv)
    gpu_link = card_link[series][brand]

    driver = webdriver.Chrome('../webdriver/chromedriver')
    username = USERNAME if user == '1' else SECONDARY_USER
    password = PASSWORD if user == '1' else SECONDARY_PW
    signin(driver, username, password)
    # Wait to move on until successfully signed in.
    try:
        # id = shop-header
        shop_header_exists = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.shop-header'))
        ) 
    except:
        print('signin timed out after 10s')
    

    driver.get(gpu_link)
    in_progress = True
    count, cart_count = 1, 0
    while in_progress and count < 6:
        
        print('iteration ', count)
        print('------------')
        try:
            add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.add-to-cart-button'))
            )
            add_to_cart_button.click()
            cart_count += 1
            print('clicked add to cart: ', cart_count)
        except:
            print(f'unable to add to cart on try {cart_count}')
            count += 1
            continue
        
        try:
            # Wait to move on until successfully added to cart.
            added_to_cart = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.added-to-cart'))
            ) 
        except:
            print('continuing to add to cart again...')
            continue

        driver.get('https://www.bestbuy.com/checkout/r/fast-track')
        print('fastracked to checkout')
        try:
            cvv_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "credit-card-cvv"))
            )
            cvv_field.send_keys(CVV)
        except:
            print('entering cvv failed after 10s')
            continue

        in_progress = False
        count += 1
        print('successfully checked out!!!')
    
    time.sleep(60)
    driver.close()
    driver.quit()