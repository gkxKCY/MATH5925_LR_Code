from selenium import webdriver
import selenium.webdriver.common.keys as keys
import time


def check_element_exists(driver, element):  # judge whether the element exists
    try:
        driver.find_element("xpath", element)
        return True
    except Exception as e:
        return False


# def check_tip_exists():
#     signal = 1
#     time.sleep(5)  # wait for the result
#     dismiss_1 = "/html/body/div[11]/div[2]/div[1]/div[4]/div/div[1]/button"
#     dismiss_2 = "/html/body/div[2]/div[2]/div/div[8]/div/div/button"
#     if check_element_exists(driver, dismiss_1, "xpath"):
#         driver.find_element("xpath", dismiss_1).click()  # dismiss the tip
#         signal = 0
#     if check_element_exists(driver, dismiss_2, "xpath"):
#         driver.find_element("xpath", dismiss_2).click()  # dismiss the tip
#         signal = 0
#     return signal


queryTest = input('Please input the keyword: ')  # get keyword

start_time = time.time()

literature_list = []
title_list = []
citation_list = []
text = ''
url = 'https://www.webofscience.com/wos/woscc/basic-search'

opt = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 1}  # set manual download
#
# However setting path seems not working in the latest selenium :(
# opt.add_argument("--headless=new")
opt.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=opt)

driver.get(url)  # get search url
time.sleep(2)

# if not English
lang = "/html/body/div[4]/div[2]/div/div[1]/div/div[2]/div/button[2]"
if check_element_exists(driver, lang):
    if driver.find_element("xpath", lang).text == "接受所有 Cookie":
        driver.find_element("xpath", lang).click()  # cookies
        driver.find_element("xpath", "/html/body/app-wos/main/div/div/div[1]/app-header/div[1]/header/div[1]/cdx-header-global/button[1]").click()
        time.sleep(1)
        driver.find_element("xpath", "/html/body/div[5]/div[2]/div/div/div/div/button[3]").click()
        time.sleep(2)

driver.find_element("xpath",
                    "/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route/app-search-home/div[2]/div/app-input-route/app-search-basic/app-search-form/form/div[1]/app-search-row/div/div[2]/mat-form-field/div/div[1]/div[3]/input") \
    .send_keys(queryTest)  # input search query
time.sleep(2)
# close the tip
tip = "/html/body/div[6]/div/div[1]/div[2]/h2/div/p"
if check_element_exists(driver, tip):
    if driver.find_element("xpath", tip).text == "Are you getting the most out of the Web of Science?":
        driver.find_element("xpath", "/html/body/div[6]/div/div[1]/div[4]/div/div/button").click()
        time.sleep(2)
driver.find_element("xpath",
                    "/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route/app-search-home/div[2]/div/app-input-route/app-search-basic/app-search-form/form/div[3]/button[2]").click()
# open the result

time.sleep(10)  # wait for the result

url_list = []  # create list of url

# start set filter
i = 7
class_element_start = "/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route/app-base-summary-component"
class_element_middle = "/div/div[1]/app-refine-panel/div/form/div["
class_element_end = "]/fieldset/div/div/div/button[1]"
list_element_middle = "/div[2]/app-refine-see-all-shared/div/div[6]/fieldset/ul/li["
list_element_end = "]/app-refine-option/div/mat-checkbox/label/span[1]"
list_element_end2 = "]/app-refine-option/div/mat-checkbox/label/span[2]/span[2]"
refine_element = "/div[2]/app-refine-see-all-shared/div/div[8]/button[3]"

# set year
driver.find_element("xpath", class_element_start + class_element_middle + str(i) + class_element_end).click()
time.sleep(1)
# from 2022 to 2013
num = 1
while True:
    if driver.find_element("xpath",
                           class_element_start + list_element_middle + str(num) + list_element_end2).text == '2022':
        for j in range(num, num + 10):
            driver.find_element("xpath", class_element_start + list_element_middle + str(j) + list_element_end).click()
            time.sleep(1)
        break
    else:
        num += 1
# refine
driver.find_element("xpath", class_element_start + refine_element).click()
time.sleep(5)
i += 1

# set document type
driver.find_element("xpath", class_element_start + class_element_middle + str(i) + class_element_end).click()
time.sleep(1)
# article, review, proceeding
j = 1
signal = 0
while check_element_exists(driver,
                           class_element_start + list_element_middle + str(j) + list_element_end) and signal != 3:
    if driver.find_element("xpath",
                           class_element_start + list_element_middle + str(j) + list_element_end2).text == "Article":
        driver.find_element("xpath", class_element_start + list_element_middle + str(j) + list_element_end).click()
        signal += 1
        time.sleep(1)
    elif driver.find_element("xpath", class_element_start + list_element_middle + str(
            j) + list_element_end2).text == "Review Article":
        driver.find_element("xpath", class_element_start + list_element_middle + str(j) + list_element_end).click()
        signal += 1
        time.sleep(1)
    elif driver.find_element("xpath", class_element_start + list_element_middle + str(
            j) + list_element_end2).text == "Proceeding Paper":
        driver.find_element("xpath", class_element_start + list_element_middle + str(j) + list_element_end).click()
        signal += 1
        time.sleep(1)
    j += 1
# refine
driver.find_element("xpath", class_element_start + refine_element).click()
time.sleep(5)
i += 1

# set language
driver.find_element("xpath", class_element_start + class_element_middle + "20]/fieldset/button").click()
time.sleep(1)
driver.find_element("xpath",
                    class_element_start + class_element_middle + "20]/fieldset/div/div/app-refine-option[1]/div/mat-checkbox/label/span[1]").click()
time.sleep(1)
driver.find_element("xpath", class_element_start + class_element_middle + "20]/fieldset/div/div/div/button[3]").click()
time.sleep(5)

# judge number of documents, if smaller than 10000, choose 500
whole_page = driver.find_element("xpath",
                                 "/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route/app-base-summary-component/app-search-friendly-display/div[1]/app-general-search-friendly-display/h1/span").text
whole_page = int(whole_page.replace(',', ''))
if whole_page < 10000:
    pages = 500
else:
    pages = 1000

# export
driver.find_element("xpath",
                    class_element_start + "/div/div[2]/app-page-controls[1]/div/app-export-option/div/app-export-menu/div/button").click()
class_element_start = "/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route/app-base-summary-component"
time.sleep(1)
# set BibTeX
driver.find_element("xpath", "/html/body/div[4]/div[2]/div/div/div/div/div[7]/button").click()
time.sleep(1)
# set pages
driver.find_element("xpath",
                    "/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/fieldset/mat-radio-group/div[3]/mat-radio-button/label/span[1]") \
    .click()
time.sleep(1)
if pages != 1000:
    driver.find_element("xpath",
                        "/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/fieldset/mat-radio-group/div[3]/mat-form-field[2]/div/div[1]/div[3]/span") \
        .clear()
    driver.find_element("xpath",
                        "/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/fieldset/mat-radio-group/div[3]/mat-form-field[2]/div/div[1]/div[3]/span") \
        .send_keys(str(pages))
time.sleep(1)

# export
driver.find_element("xpath",
                    "/html/body/app-wos/main/div/div/div[2]/div/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/div[2]/button[1]").click()
time.sleep(2)

end_time = time.time()
print('program access time: {}\n'.format(end_time - start_time))
