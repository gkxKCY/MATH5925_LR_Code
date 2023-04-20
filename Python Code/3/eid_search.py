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
    time.sleep(2)  # wait for the result
    dismiss_1 = "/html/body/div[11]/div[2]/div[1]/div[4]/div/div[1]/button"
    dismiss_2 = "/html/body/div[2]/div[2]/div/div[8]/div/div/button"
    if check_element_exists(driver, dismiss_1, "xpath"):
        driver.find_element("xpath", dismiss_1).click()  # dismiss the tip
        signal = 0
    if check_element_exists(driver, dismiss_2, "xpath"):
        driver.find_element("xpath", dismiss_2).click()  # dismiss the tip
        signal = 0
    return signal


opt = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 1}  # set manual download
#
# However setting path seems not working in the latest selenium :(
# opt.add_argument("--headless=new")
opt.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=opt)

i = 0
with open("./eid.txt") as f:
    for line in f:
        start_time = time.time()
        doi_combine = line.replace('\n', '')
        doi_combine = 'CITEID({})'.format(doi_combine)

        url = 'https://www.scopus.com/search/form.uri?display=advanced'

        driver.get(url)  # get search url
        if i == 0:
            time.sleep(2)

            detect_lang = "/html/body/div[1]/div/div[1]/div[1]/div/sc-page-title/header/h1/span/span"  # access to the language of the website

            if driver.find_element("xpath", detect_lang).text == '高级搜索':  # if Chinese
                driver.find_element("xpath",
                                    "/html/body/div[1]/div/div[1]/micro-ui/scopus-footer/footer/div[1]/div/div/div[2]/ul/li[1]/a").click()  # switch to English
        time.sleep(0.1)
        # input result
        driver.find_element("xpath",
                            "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div/form/div/div[1]/div/div/div[2]/div/section/div[1]/div[1]").click()
        time.sleep(0.1)
        driver.find_element("xpath",
                            "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div/form/div/div[1]/div/div/div[2]/div/section/div[1]/div[1]/div").clear()
        time.sleep(0.1)
        driver.find_element("xpath",
                            "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div/form/div/div[1]/div/div/div[2]/div/section/div[1]/div[1]/div").send_keys(
            doi_combine)
        time.sleep(0.1)
        # open the result
        driver.find_element("xpath",
                            "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div/form/div/div[1]/div/div/div[2]/div/section/div[2]/ul/li[5]/button").click()

        time.sleep(1)  # wait for the result

        signal = "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[1]/section/div[2]/div/span"
        if check_element_exists(driver, signal, "xpath"):
            if "No documents match" in driver.find_element("xpath", signal).text:
                continue

        time.sleep(0.1)

        if i == 0:
            old = "/html/body/div[1]/div/div[1]/div/div/div[3]/form/micro-ui/document-search-results-page-release-switch/div/section/div/div/div/div/button"
            if check_element_exists(driver, old, "xpath"):  # switch to new version
                driver.find_element("xpath", old).click()

            old_2 = "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page-release-switch/div/section/div/div/div/div/button"
            if check_element_exists(driver, old_2, "xpath"):  # switch to new version
                driver.find_element("xpath", old_2).click()

            time.sleep(2)  # wait for the result
            signal = check_tip_exists()
            i += 1

        time.sleep(0.1)

        # set all
        driver.find_element("xpath",
                            "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[1]/label").click()
        time.sleep(0.1)
        driver.find_element("xpath",
                            "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[1]/span/button").click()
        time.sleep(0.1)
        # set plain text
        driver.find_element("xpath",
                            "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[1]/span/div/div[1]/button[4]").click()
        time.sleep(0.8)
        # set doi only
        # export
        driver.find_element("xpath",
                            "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[2]/div/div/span[2]/div/div/button").click()
        time.sleep(3)

        end_time = time.time()
        print('program access time: {}\n'.format(end_time - start_time))
