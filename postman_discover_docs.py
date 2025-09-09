from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_TEMPLATE = "https://www.postman.com/explore/collections?sort=forkCount&page={page_num}&filter="

# Setting up the browser and its options.
options = webdriver.ChromeOptions()
options.headless = False  # You can set this to True if you want to run the browser in the background

# Define the web driver.
driver = webdriver.Chrome(options=options)

# Define a wait object to utilize the explicit waits.
wait = WebDriverWait(driver, 10)  # Adjust the time as needed.

# A loop to go through all the pages.
for page_num in range(1, 34964):  # Adjust the range as needed.
    driver.get(URL_TEMPLATE.format(page_num=page_num))
    
    # Wait for the list of APIs to load and get all the API workspace links.
    api_workspace_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.entity-heading')))
    api_workspace_links = [elem.get_attribute('href') for elem in api_workspace_elements]

    for link in api_workspace_links:
        driver.get(link)
        
        try:
            documentation_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".documentation-overview-footer")))
            documentation_link = documentation_element.get_attribute('href')
            print(f"API Documentation Link: {documentation_link}")
        except:
            print(f"Skipping {link} due to error or missing documentation link.")
            continue

driver.quit()
