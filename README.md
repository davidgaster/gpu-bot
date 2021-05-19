# GPU Bot
Buy 3000 series graphics cards on Best Buy with Selenium Python.
Supplied webdriver only compatible with Chrome Version 90.

# Usage
python3 buy_card.py <brand> <series>

Example:
python3 buy_card.py nvidia 3070

Supported brands (price low to high):
- nvidia
- evga
- asus
- msi

Supported series:
- 3060ti
- 3070
- 3080
- 3090

If any typo or error occurs, defaults cli args to:
python3 buy_card.py nvidia 3060ti

Configure username & password to login in the .env file