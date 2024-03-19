import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

# Path to the chromedriver executable
#driver_path = '/home/spear/Downloads/packages/chromedriver-linux64'

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Go to the Python website
driver.get("https://summerofcode.withgoogle.com/programs/2024/organizations")

# Print the title of the page
print(driver.title)

time.sleep(2)
elements = driver.find_elements(By.XPATH, "//*[@title='Opens in a new window']")
#element =  driver.find_element(By.PARTIAL_LINK_TEXT, '/programs/2024/organizations/')
#print("VALUE ---- >\n", element)

for element in elements:

    all_attributes = element.get_property("attributes")

    # Print attributes
    print("Element:", element.tag_name)
    for attribute in all_attributes:
        print(attribute["name"], ":", attribute["value"])

# Close the browser
driver.close()
