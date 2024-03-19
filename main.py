import sys
import time
import re
from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Queue

# Globals
inputted_language = ""
queue = Queue()
root_url = 'https://summerofcode.withgoogle.com/'


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


def initialise():
    set_language()
    driver = webdriver.Chrome()
    driver.get("https://summerofcode.withgoogle.com/programs/2024/organizations")
    time.sleep(10)
    project_url_collector(driver)


all_projects_urls = []
elements_list = []


def process_urls_on_page(elements_list_value):
    for element in elements_list_value:
        all_attributes = element.get_property("attributes")
        for attribute in all_attributes:
            if 'href' in attribute["name"]:
                all_projects_urls.append(attribute["value"])
    del elements_list[:]
    print("Returning after collecting urls on page")
    print("Till Now..", all_projects_urls)
    print("Len = ", len(all_projects_urls))


def project_url_collector(driver):
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            process_urls_on_page(
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@title='Opens in a new window']"))))
            wait = WebDriverWait(driver, 10)
            next_page_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']")))
            next_page_element.click()
            time.sleep(5)
        except Exception as ex:
            print("Exception occurred [project_url_collector]: ", ex)
            break
        continue


def get_tech(url, driver, queue_res):
    driver = driver()
    print("WORKING FOR : ", url)
    driver.get(url)
    w = WebDriverWait(driver, 10)
    elem = w.until(EC.presence_of_element_located((By.XPATH, "//*[@class='tech__content']")))
    tech_list_string = elem.text
    if find_match(inputted_language, tech_list_string):
        queue_res.put(url)


def get_result():
    print("\n\n--------------------------- Final Results :----------------------------------")
    while not queue.empty():
        print(queue.get())


def clean_url(result_urls):
    print("CLEANING URLs...", result_urls)
    jobs = []
    print("TOTAL PROJECTS : ", len(result_urls))
    for url in result_urls:
        if 'http' not in url:
            if url[0] == '/':
                url = root_url + url[1:]
            jobs.append(url)
        else:
            continue
    return jobs


def process_result_batches(jobs):
    processes = []
    for i in jobs:
        process = Process(target=get_tech, args=[i, webdriver.Chrome, queue])
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
    print("Done processing this batch.....")


def set_language():
    global inputted_language
    inputted_language = input("Enter the name of programming language : ")


def run_jobs(jobs):
    limit = 5
    start = 0
    end = limit
    if len(jobs) < limit:
        process_result_batches(jobs)
    while end < len(jobs):
        process_result_batches(jobs[start:end])
        start = end
        end = start + limit


try:
    initialise()
except Exception as err:
    print("Exception occurred during initialisation..", err)
    sys.exit(1)
run_jobs(clean_url(all_projects_urls))
get_result()
