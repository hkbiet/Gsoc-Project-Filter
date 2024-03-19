import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find_match(user_input, result_string):
    print("Looking for : ", user_input, " in tech string : ", result_string)
    regex_pattern = r' ' + re.escape(user_input)
    match = re.search(regex_pattern, result_string, re.IGNORECASE)
    if match:
        print(f"Found '{match.group()}' in the string.")
        return True
    else:
        print("No match found.")
        return False


class Begin:
    def __init__(self):
        print("Gsoc 2024 filteration of projects based on programming languages.")
        self.lang = input("Enter the name of programming language : ")
        self.results = []

    def get_input_lang(self):
        return self.lang

    def set_results(self, value):
        self.results.append(value)

    def get_results(self):
        return self.results


driver = webdriver.Chrome()
driver.get("https://summerofcode.withgoogle.com/programs/2024/organizations")
root_url = 'https://summerofcode.withgoogle.com/'
time.sleep(5)

result = []
elements_list = []


def process(elements_list_value):
    for element in elements_list_value:
        all_attributes = element.get_property("attributes")
        for attribute in all_attributes:
            if 'href' in attribute["name"]:
                result.append(attribute["value"])
    del elements_list[:]


while True:
    try:
        wait = WebDriverWait(driver, 10)
        process(wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@title='Opens in a new window']"))))
        wait = WebDriverWait(driver, 10)
        next_page_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']")))
        next_page_element.click()
        time.sleep(5)
    except Exception as ex:
        print("Exception occurred : ", ex)
        break
    continue


def get_tech(url, obj):
    lang = obj.get_input_lang()
    print("WORKING FOR : ", url)
    driver.get(url)
    w = WebDriverWait(driver, 10)
    elem = w.until(EC.presence_of_element_located((By.XPATH, "//*[@class='tech__content']")))
    tech_list_string = elem.text
    if find_match(lang, tech_list_string):
        obj.set_results(url)


def get_result(obj):
    print("FINAL RESULTS : ", obj.get_results())


def clean_url(result_urls):
    print("TOTAL PROJECTS : ", len(result_urls))
    obj = Begin()
    for url in result_urls:
        if 'http' not in url:
            if url[0] == '/':
                url = root_url + url[1:]
            get_tech(url, obj)
        else:
            continue
    get_result(obj)


print("ALL URLs : ",result)
clean_url(result)
driver.close()
