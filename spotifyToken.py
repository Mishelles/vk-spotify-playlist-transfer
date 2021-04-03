from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import json

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get("https://accounts.spotify.com/ru/login")
login_input = driver.find_element_by_id("login-username")
login_input.send_keys("wotev90990@whyflkj.com")
pass_input = driver.find_element_by_id("login-password")
pass_input.send_keys(",!2T2:,eg7s@63\"")
button = driver.find_element_by_id("login-button")
button.click()
time.sleep(0.5)
driver.get("https://open.spotify.com/get_access_token?reason=transport&productType=web_player")
time.sleep(0.5)
tab = driver.find_element_by_id("rawdata-tab")
tab.click()
response = driver.find_element_by_class_name("data")
accessToken = json.loads(response.text)['accessToken']
driver.close()
print(accessToken)

# Username	2yq5sodfqo7nox3yh3xy3xito
# Email	wotev90990@whyflkj.com
# Pass:,!2T2:,eg7s@63"