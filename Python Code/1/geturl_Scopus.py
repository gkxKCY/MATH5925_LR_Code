from selenium import webdriver
import selenium.webdriver.common.keys as keys
import time


def check_element_exists(driver, element, condition):  # judge whether the element exists
    try:
        if condition == 'class':
            driver.find_element_by_class_name(element)
        elif condition == 'id':
            driver.find_element_by_id(element)
        elif condition == 'xpath':
            driver.find_element("xpath", element)
        return True
    except Exception as e:
        return False


def check_tip_exists():
    signal = 1
    time.sleep(5)  # wait for the result
    dismiss_1 = "/html/body/div[11]/div[2]/div[1]/div[4]/div/div[1]/button"
    dismiss_2 = "/html/body/div[2]/div[2]/div/div[8]/div/div/button"
    if check_element_exists(driver, dismiss_1, "xpath"):
        driver.find_element("xpath", dismiss_1).click()  # dismiss the tip
        signal = 0
    if check_element_exists(driver, dismiss_2, "xpath"):
        driver.find_element("xpath", dismiss_2).click()  # dismiss the tip
        signal = 0
    return signal


queryTest = input('Please input the keyword: ')  # get keyword

start_time = time.time()

literature_list = []
title_list = []
citation_list = []
text = ''
url = 'https://www.scopus.com/search/form.uri?display=basic&zone=header&origin=recordpage#basic'

opt = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 1}  # set manual download
#
# However setting path seems not working in the latest selenium :(
# opt.add_argument("--headless=new")
opt.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=opt)

driver.get(url)  # get search url
time.sleep(2)

detect_lang = "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/micro-ui/scopus-homepage/div/els-typography"  # access to the language of the website

if driver.find_element("xpath", detect_lang).text == '开始浏览':  # if Chinese
    driver.find_element("xpath",
                        "/html/body/div[1]/div/div[1]/micro-ui/scopus-footer/footer/div[1]/div/div/div[2]/ul/li[1]/a").click()  # switch to English

driver.find_element("xpath",
                    "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/micro-ui/scopus-homepage/div/div/els-tab/els-tab-panel[1]/div/form/div[1]/div/div[2]/div/div/label/input") \
    .send_keys(queryTest)  # input search query
time.sleep(2)
driver.find_element("xpath",
                    "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/micro-ui/scopus-homepage/div/div/els-tab/els-tab-panel[1]/div/form/div[2]/div[2]/button").click()
# open the result

time.sleep(5)  # wait for the result
# dismiss_1 = "/html/body/div[11]/div[2]/div[1]/div[4]/div/div[1]/button"
# dismiss_2 = "/html/body/div[2]/div[2]/div/div[8]/div/div/button"
# if check_element_exists(driver, dismiss_1, "xpath"):
#     driver.find_element("xpath", dismiss_1).click()  # dismiss the tip
# if check_element_exists(driver, dismiss_2, "xpath"):
#     driver.find_element("xpath", dismiss_2).click()  # dismiss the tip
url_list = []  # create list of url

time.sleep(2)

old = "/html/body/div[1]/div/div[1]/div/div/div[3]/form/micro-ui/document-search-results-page-release-switch/div/section/div/div/div/div/button"
if check_element_exists(driver, old, "xpath"):  # switch to new version
    driver.find_element("xpath", old).click()

time.sleep(5)  # wait for the result
signal = check_tip_exists()

time.sleep(5)

# order by relevance
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[3]/div/div/div[1]").click()
time.sleep(1)
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[3]/div/div/div[1]/els-select/div/label/select/option[5]").click()

time.sleep(5)

k = 3
class_element = "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div"
while check_element_exists(driver, class_element + '/els-focus-tab-detector[{}]/div/button/h4'.format(k), "xpath"):
    if driver.find_element("xpath", class_element + '/els-focus-tab-detector[{}]/div/button/h4'.format(k)).text == 'Document type':
        driver.find_element("xpath",
                            class_element + '/els-focus-tab-detector[{}]/div/section/div/div/div/button'.format(k)).click()
        break
    else:
        k += 1
time.sleep(3)
j = 0
dtype_element = "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div/els-focus-trap/els-modal/div/div/div/div/div[1]/div/div/div[2]/els-facet/els-stack"

while check_element_exists(driver, dtype_element + "/label[{}]/input".format(j + 1), "xpath"):
    time.sleep(1)
    # Select Article
    if driver.find_element("xpath",
                            dtype_element + "/label[{}]/div/els-typography".format(j + 1)).text == "Article":
        driver.find_element("xpath", dtype_element + "/label[{}]/input".format(j + 1)).click()
    # Select Review
    if driver.find_element("xpath", dtype_element + "/label[{}]/div/els-typography".format(
            j + 1)).text == "Review":
        driver.find_element("xpath", dtype_element + "/label[{}]/input".format(j + 1)).click()
    # Select Conference Paper
    if driver.find_element("xpath", dtype_element + "/label[{}]/div/els-typography".format(
            j + 1)).text == "Conference paper":
        driver.find_element("xpath", dtype_element + "/label[{}]/input".format(j + 1)).click()
    j += 1
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div/els-focus-trap/els-modal/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/button[2]").click()

# set language only in English
# driver.find_element("xpath", "/html/body/div[1]/div/div[1]/div/div/div[3]/form/div[4]/div[1]/div/div/div/div[3]/div/div[2]/div[2]/div[1]/div[3]/div[4]/div[13]/div").click()
time.sleep(2)
class_element = "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div"
while check_element_exists(driver, class_element + '/els-focus-tab-detector[{}]/div/button/h4'.format(k),
                            "xpath"):
    if driver.find_element("xpath", class_element + '/els-focus-tab-detector[{}]/div/button/h4'.format(
            k)).text == 'Language':
        driver.find_element("xpath",
                            class_element + '/els-focus-tab-detector[{}]/div/section/div/div/div/els-facet/els-stack/label[1]'.format(
                                k)).click()
        break
    else:
        k += 1
time.sleep(2)
# set result
driver.find_element("xpath", "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div/div/els-sticky/div[1]/div/div/div/div/div/button[2]").click()

time.sleep(2)

# set 2013-2023
driver.find_element("xpath", "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div/els-focus-tab-detector[2]/div/section/div/div/div/div[2]/els-facet-range/div/els-stack/div[1]/els-input-v2").send_keys('2013')
time.sleep(1)  # set 2013
# driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div/els-focus-tab-detector[2]/div/section/div/div/div/div[1]/label[2]/input").click()
# time.sleep(1)  # click
# driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div/els-focus-tab-detector[2]/div/section/div/div/div/div[1]/label[1]/input").click()
# time.sleep(1)  # click
element_2022 = "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div/els-focus-tab-detector[2]/div/section/div/div/div/div[2]/els-facet-range/div/els-stack/div[3]/els-input-v2"
driver.find_element("xpath", element_2022).send_keys(keys.Keys.RIGHT)
time.sleep(1)  # set right
driver.find_element("xpath", element_2022).send_keys(keys.Keys.BACKSPACE)
time.sleep(1)  # clear
driver.find_element("xpath", element_2022).send_keys('2')
time.sleep(1)  # set 2022
driver.find_element("xpath", "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div/div/div[2]/div/els-focus-tab-detector[2]/div/section/div/div/div/div[2]/els-facet-range/div/els-stack/div[4]/els-button").click()
time.sleep(1)  # set age

# judge number of documents, if smaller than 10000, choose 500
whole_page = driver.find_element("xpath", "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[1]/div[4]/div[2]/div/div[1]/h2").text
whole_page = int(whole_page.replace(',', '').split(' ')[0])
if whole_page < 10000:
    pages = 500
else:
    pages = 1000

# set all
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[1]/label").click()
time.sleep(1)
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[1]/span/button").click()
time.sleep(1)
# set BibTeX
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[1]/span/div/div[1]/button[3]").click()
time.sleep(1)
# set pages
driver.find_element("xpath",
                    "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div/label/input")\
    .clear()
time.sleep(1)
driver.find_element("xpath",
                    "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div/label/input") \
    .send_keys(str(pages))
time.sleep(1)
# set bibliographical information
driver.find_element("xpath",
                    "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[1]/div/div/div[2]/div/div[2]/span/label").click()
time.sleep(1)
# set Abstract & keywords
driver.find_element("xpath",
                    "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[1]/div/div/div[2]/div/div[3]/span/label").click()
time.sleep(1)
# set references
driver.find_element("xpath",
                    "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[1]/div/div/div[2]/div/div[5]/div/label[4]").click()
time.sleep(1)
# export
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[2]/div/div/span[2]/div/div/button").click()
time.sleep(2)

end_time = time.time()
print('program access time: {}\n'.format(end_time - start_time))
