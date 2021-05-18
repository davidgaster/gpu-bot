# GPU Bot
Buy 3000 series graphics cards on Best Buy with Selenium Python.
Supplied webdriver only compatible with Chrome Version 90.

# Usage
python3 main.py <brand> <series>

Example:
python3 main.py nvidia 3070

Supported brands:
- nvidia
- asus
- evga
- msi

Supported series:
- 3060ti
- 3070
- 3080
- 3090

If any typo or error occurs, defaults cli args to:
python3 main.py nvidia 3060ti

Configure username & password to login in the .env file