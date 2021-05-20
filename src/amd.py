'''
AMD Checkout process - Keep refreshing page every 5 seconds
1. add to cart button
<button class="btn-shopping-cart btn-shopping-neutral use-ajax" href="/en/direct-buy/add-to-cart/5450881700">
                Add to cart
              </button>

2. Recaptcha. Wait 2s
<div class="recaptcha-checkbox-border" role="presentation"></div>

3. Add to cart
id = confirm-add-to-cart-btn
<a id="confirm-add-to-cart-btn" class="btn-shopping-cart btn-shopping-neutral" data-productid="5450881700" href="">ADD TO CART</a>

4. checkout button
<a href="/en/direct-buy/checkout/payment/105562502113/us" class="btn-transparent-black checkout">
        Go to checkout
      </a>

CSS Selector --> .checkout


PAYMENT PAGE - ID FIELDS
ccNumber
ccExpiry
card-security-code
edit-email
edit-phone-number
edit-first-name
edit-last-name
edit-shop-country
edit-address-line
edit-city
edit-state
edit-postal-code


NOTES
1. Capthca after CC entry (manually)
2. Select Country and State (manually)
3. next step is an <input>. click it --> id = edit-submit


Shipping page
Just click next step (id=edit-submit)

Place order page
1. captcha
2. terms and conditions id = terms-and-conditions-check
3. confirm CSS selector = .confirm-order-btn

<div class="recaptcha-checkbox-border" role="presentation"></div>
<div class="recaptcha-checkbox-border" role="presentation"></div>
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
CARD = os.getenv('CARD')
EXPIRES = os.getenv('EXPIRES')
CVV = os.getenv('CVV')
EMAIL = os.getenv('EMAIL')
PHONE = os.getenv('PHONE')
FNAME = os.getenv('FNAME')
LNAME = os.getenv('LNAME')
COUNTRY = os.getenv('COUNTRY')
ADDRESS = os.getenv('ADDRESS')
CITY = os.getenv('CITY')
POSTAL = os.getenv('POSTAL')

def get_input(args):
    brand, series = '', ''
    if len(args) < 3:
        return ('amd', '5600x')
    elif len(args) != 3:
        return ('amd', '6700xt')
    else:
        brand, series = args[1].lower(), args[2].lower()
    
    if series not in card_link:
        series = '6700xt'
    if brand not in card_link[series]:
        brand = 'amd'

    return brand, series

##########################
#####      MAIN      #####
##########################
if __name__ == '__main__':

    brand, series = get_input(sys.argv)
    gpu_link = card_link[series][brand]

    driver = webdriver.Chrome('../webdriver/chromedriver')
    # Wait to move on until successfully signed in.

    driver.get(gpu_link)
    time.sleep(2)
    in_progress = True
    count = 1
    while in_progress and count < 2:
        
        print('\niteration ', count)
        print('------------')
        
        ##################
        # ADDING TO CART #
        ##################
        try:
            add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-shopping-cart'))
            )
            add_to_cart_button.click()
            print('clicked add to cart')

        except:
            print('unable to add to cart')
            count += 1
            continue
        
        
        print('YOU NEED TO click recaptcha!!!')
        time.sleep(30)

        try:
            confirm_add_to_cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'confirm-add-to-cart-btn'))
            )
            confirm_add_to_cart_button.click()
            print('CONFIRMED add to cart')

        except:
            print('unable to CONFIRM add to cart')
            count += 1
            continue
        time.sleep(0.6)

        try:
            checkout_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.checkout'))
            )
            checkout_button.click()
            print('clicked checkout')

        except:
            print('unable to click checkout')
            count += 1
            continue
        time.sleep(0.5)


        ################
        # PAYMENT PAGE #
        ################
        try:
             = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, ''))
            )
            .send_keys(CVV)
            print('')

        except:
            print('')
            count += 1
            continue 

        #################
        # SHIPPING PAGE #
        #################
        try:
             = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, ''))
            )
            .send_keys(CVV)
            print('')

        except:
            print('')
            count += 1
            continue 

        ####################
        # PLACE ORDER PAGE #
        ####################
        try:
             = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, ''))
            )
            .send_keys(CVV)
            print('')

        except:
            print('')
            count += 1
            continue 

        in_progress = False
        count += 1
        print('successfully checked out!!!')
    
    driver.close()
    driver.quit()