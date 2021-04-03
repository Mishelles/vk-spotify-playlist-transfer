from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import json
import base64

cypher = 'd290ZXY5MDk5MEB3aHlmbGtqLmNvbV9fLCEyVDI6LGVnN3NANjMi'


def get_token():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://accounts.spotify.com/ru/login")
    login_input = driver.find_element_by_id("login-username")
    creds = base64.b64decode(cypher.encode()).decode().split('__')
    login_input.send_keys(creds[0])
    pass_input = driver.find_element_by_id("login-password")
    pass_input.send_keys(creds[1])
    button = driver.find_element_by_id("login-button")
    button.click()
    time.sleep(0.5)
    driver.get("https://open.spotify.com/get_access_token?reason=transport&productType=web_player")
    time.sleep(0.5)
    tab = driver.find_element_by_id("rawdata-tab")
    tab.click()
    response = driver.find_element_by_class_name("data")
    access_token = json.loads(response.text)['accessToken']
    driver.close()
    return access_token
