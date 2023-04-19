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
pnum = input('Please input number: ')  # get number
snum = input('Please input scopus number: ')  # get scopus
if snum != '500':
    snum = '1000'

doi_combine = ''
count = 0
doi_list = []

f_scopus = open('./scopus/scopus_{}_{}_201322.csv'.format(queryTest, snum), 'r')
scopus = f_scopus.read()

f_wos = open('./scopus/scopus_{}_wos_201322.csv'.format(queryTest), 'r')
wos = f_wos.read()

with open('./pubmed/pubmed_{}_{}_201322.csv'.format(queryTest, pnum)) as f:
    for line in f:
        if 'DOI' in line:
            continue
        doi = line.split('\n')[0]
        if doi in scopus or doi in wos:
            count += 1
            continue
        if doi_combine != '':
            doi_combine += ' OR '
        doi_combine += 'DOI(' + doi + ')'
        doi_list.append(doi)

print(count)
f_norepeat = open('./pubmed/pubmed_{}_norepeat_201322.csv'.format(queryTest), 'w')
f_norepeat.write('DOI\n')
for i in range(len(doi_list)):
    f_norepeat.write(doi_list[i] + '\n')

f_scopus.close()
f_wos.close()
f_norepeat.close()


start_time = time.time()

literature_list = []
title_list = []
citation_list = []
text = ''
url = 'https://www.scopus.com/search/form.uri?display=advanced'

opt = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 1}  # set manual download
#
# However setting path seems not working in the latest selenium :(
# opt.add_argument("--headless=new")
opt.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=opt)

driver.get(url)  # get search url
time.sleep(2)

detect_lang = "/html/body/div[1]/div/div[1]/div[1]/div/sc-page-title/header/h1/span/span"  # access to the language of the website

if driver.find_element("xpath", detect_lang).text == '高级搜索':  # if Chinese
    driver.find_element("xpath",
                        "/html/body/div[1]/div/div[1]/micro-ui/scopus-footer/footer/div[1]/div/div/div[2]/ul/li[1]/a").click()  # switch to English
time.sleep(1)
# input result
driver.find_element("xpath",
                    "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div/form/div/div[1]/div/div/div[2]/div/section/div[1]/div[1]").click()
time.sleep(1)
driver.find_element("xpath",
                    "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div/form/div/div[1]/div/div/div[2]/div/section/div[1]/div[1]/div").send_keys(doi_combine)
time.sleep(1)
# open the result
driver.find_element("xpath",
                    "/html/body/div[1]/div/div[1]/div[2]/div/div[3]/div/div[2]/div/form/div/div[1]/div/div/div[2]/div/section/div[2]/ul/li[5]/button").click()

time.sleep(5)  # wait for the result
# dismiss_1 = "/html/body/div[11]/div[2]/div[1]/div[4]/div/div[1]/button"
# dismiss_2 = "/html/body/div[2]/div[2]/div/div[8]/div/div/button"
# if check_element_exists(driver, dismiss_1, "xpath"):
#     driver.find_element("xpath", dismiss_1).click()  # dismiss the tip
# if check_element_exists(driver, dismiss_2, "xpath"):
#     driver.find_element("xpath", dismiss_2).click()  # dismiss the tip
url_list = []  # create list of url


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

pages = driver.find_element("xpath",
                            "/html/body/div[1]/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[1]/div[4]/div[2]/div/div[1]/h2").text
pages = int(pages.split(' ')[0].replace(',', ''))

# set all
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[1]/label").click()
time.sleep(1)
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[1]/span/button").click()
time.sleep(1)
# set BibTeX
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[1]/span/div/div[1]/button[3]").click()
time.sleep(1)

# set bibliographical information
driver.find_element("xpath",
                    "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[1]/div/div/div/div/div[2]/span/label").click()
time.sleep(1)
# set Abstract & keywords
driver.find_element("xpath",
                    "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[1]/div/div/div/div/div[3]/span/label").click()
time.sleep(1)
# set references
driver.find_element("xpath",
                    "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[1]/div/div/div/div/div[5]/div/label[4]").click()
time.sleep(1)
# export
driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/div[3]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[2]/div/div[2]/div/div[1]/table/tbody/tr/td[2]/div/div/div[2]/div/div/section/div[2]/div/div/span[2]/div/div/button").click()
time.sleep(2)

end_time = time.time()
print('program access time: {}\n'.format(end_time - start_time))
