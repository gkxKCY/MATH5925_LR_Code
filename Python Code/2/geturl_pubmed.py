from selenium import webdriver
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


queryTest = input('Please input the keyword: ')  # get keyword
start_time = time.time()
literature_list = []
title_list = []
citation_list = []
text = ''


opt = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 1}  # set manual download
#
# However setting path seems not working in the latest selenium :(
# opt.add_argument("--headless=new")
opt.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=opt)

pages = 10
signal = 1
for i in range(pages):
    url = 'https://pubmed.ncbi.nlm.nih.gov/?term={}&filter=pubt.booksdocs&filter=pubt.review&filter=lang.english&filter=years.2013-2022&size=100&page={}'.format(queryTest, i + 1)

    driver.get(url)  # get search url
    time.sleep(5)  # wait for the result

    start_for_time = time.time()

    result_num = driver.find_element("xpath", "/html/body/main/div[9]/div[2]/div[2]/div[1]/div[1]/span").text
    result_num = int(result_num.replace(',', ''))
    actual_pages = 0
    # set the actual pages
    if int(result_num % 100) != 0:
        actual_pages = int(result_num / 100) + 1
    else:
        actual_pages = int(result_num / 100)
    # set 500
    if result_num < 10000:
        signal = 0
    # judge the expect pages and actual pages
    time.sleep(1)
    # click save
    driver.find_element("xpath", "/html/body/main/form/div[2]/div/div[4]/button[1]").click()
    time.sleep(1)
    # click selection
    driver.find_element("xpath", "/html/body/main/div[1]/div/form/div[2]/select").click()
    time.sleep(1)
    # click pubmed
    driver.find_element("xpath", "/html/body/main/div[1]/div/form/div[2]/select/option[2]").click()
    time.sleep(1)
    # click create file
    driver.find_element("xpath", "/html/body/main/div[1]/div/form/div[3]/button[1]").click()
    time.sleep(3)

    end_for_time = time.time()
    print('The {} page : {}'.format(i + 1, end_for_time - start_for_time))

    if actual_pages <= i or (i == 4 and signal == 0):
        break

end_time = time.time()
print('The full program: {}'.format(end_time - start_time))
