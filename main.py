import sys
import time
import re
from multiprocessing import Process, Queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebScraper:
    def __init__(self):
        self.inputted_language = ""
        self.queue = Queue()
        self.root_url = 'https://summerofcode.withgoogle.com/'
        self.all_projects_urls = []
        self.elements_list = []

    def find_match(self, user_input, result_string):
        print("Looking for : ", user_input, " in tech string : ", result_string)
        regex_pattern = r' ' + re.escape(user_input)
        match = re.search(regex_pattern, result_string, re.IGNORECASE)
        if match:
            print(f"Found '{match.group()}' in the string.")
            return True
        else:
            print("No match found.")
            return False

    def initialise(self):
        self.set_language()
        self.driver = webdriver.Chrome()
        self.driver.get("https://summerofcode.withgoogle.com/programs/2024/organizations")
        time.sleep(10)
        self.project_url_collector()

    def process_urls_on_page(self, elements_list_value):
        for element in elements_list_value:
            all_attributes = element.get_property("attributes")
            for attribute in all_attributes:
                if 'href' in attribute["name"]:
                    self.all_projects_urls.append(attribute["value"])
        del self.elements_list[:]
        print("Returning after collecting urls on page")
        print("Till Now..", self.all_projects_urls)
        print("Len = ", len(self.all_projects_urls))

    def project_url_collector(self):
        while True:
            try:
                wait = WebDriverWait(self.driver, 10)
                self.process_urls_on_page(
                    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@title='Opens in a new window']"))))
                wait = WebDriverWait(self.driver, 10)
                next_page_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next page']")))
                next_page_element.click()
                time.sleep(5)
            except Exception as ex:
                print("Exception occurred [project_url_collector]: ", ex)
                break
            continue

    def get_tech(self, url):
        print("WORKING FOR : ", url)
        self.driver.get(url)
        w = WebDriverWait(self.driver, 10)
        elem = w.until(EC.presence_of_element_located((By.XPATH, "//*[@class='tech__content']")))
        tech_list_string = elem.text
        if self.find_match(self.inputted_language, tech_list_string):
            self.queue.put(url)

    def get_result(self):
        print("\n\n--------------------------- Final Results :----------------------------------")
        while not self.queue.empty():
            print(self.queue.get())

    def clean_url(self, result_urls):
        print("CLEANING URLs...", result_urls)
        jobs = []
        print("TOTAL PROJECTS : ", len(result_urls))
        for url in result_urls:
            if 'http' not in url:
                if url[0] == '/':
                    url = self.root_url + url[1:]
                jobs.append(url)
            else:
                continue
        return jobs

    def process_result_batches(self, jobs):
        processes = []
        for i in jobs:
            process = Process(target=self.get_tech, args=[i])
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
        print("Done processing this batch.....")

    def set_language(self):
        self.inputted_language = input("Enter the name of programming language : ")

    def run_jobs(self, jobs):
        limit = 5
        start = 0
        end = limit
        if len(jobs) < limit:
            self.process_result_batches(jobs)
        while end < len(jobs):
            self.process_result_batches(jobs[start:end])
            start = end
            end = start + limit

    def execute(self):
        try:
            self.initialise()
        except Exception as err:
            print("Exception occurred during initialisation..", err)
            sys.exit(1)
        self.run_jobs(self.clean_url(self.all_projects_urls))
        self.get_result()

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.execute()
