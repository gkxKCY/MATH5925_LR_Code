from selenium import webdriver
import time

url = 'https://openknowledgemaps.org/index'

opt = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 1}  # set manual download
#
# However setting path seems not working in the latest selenium :(
# opt.add_argument("--headless=new")
opt.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=opt)

driver.get(url)  # get search url
time.sleep(2)

driver.find_element("xpath", "/html/body/div[4]/div/form/div/input").send_keys('Raspberry Pi')
time.sleep(0.1)
driver.find_element("xpath", "/html/body/div[4]/div/form/div/button").click()
