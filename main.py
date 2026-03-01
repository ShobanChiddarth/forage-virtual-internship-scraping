from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
from urllib.parse import urlparse


def create_driver(headless=True):
    """Chromium driver on Linux"""
    chrome_options = Options()

    chrome_options.binary_location = "/usr/bin/chromium"

    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # If chromedriver is in PATH
    service = Service()

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

scraping_targets = []
with open("input-links.txt", "r") as fh:
    scraping_targets[:] = list(map(str.strip, fh.readlines()))

final_result: list[dict] = []

main_driver = create_driver(headless=False)
action = ActionChains(main_driver)



def scrape_one_url(url, driver=main_driver):
    result = {}

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        # Wait for page body to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Click reject cookies if it exists
        reject_cookies_buttons = driver.find_elements(By.ID, 'onetrust-reject-all-handler')
        if reject_cookies_buttons:
            reject_cookies_buttons[0].click()

        # core scraping


        job_title = driver.find_element(By.XPATH, "/html/body/main/main/div[1]/div[2]/div[1]/h1").text
        result["job_title"] = job_title
        company = urlparse(url).path.strip("/").split("/")[1]
        result["company"] = company
        result["url"] = url

        details_container = driver.find_element(By.XPATH, '//*[@id="overview-section"]/div/div[1]/div[1]/div/span')
        time_0, time_1, grades, assessments, level = details_container.text.split("\n")
        time = time_0 + ' ' + time_1

        result.update(dict(zip(("time", "grades", "assessments", "level"), (time, grades, assessments, level))))

        skills_view_all_button = driver.find_element(By.XPATH, '//*[@id="overview-section"]/div/div[2]/div/div[2]/button')
        action.move_to_element(skills_view_all_button).perform()
        skills_view_all_button.click()

        skills_container = driver.find_element(By.XPATH, '//*[@id="radix-:R3i99uutpuu4q:"]/div[2]')
        skills = [element.text for element in skills_container.find_elements(By.XPATH, './/*')]
        result["skills"] = skills

        skills_section_close_button = driver.find_element(By.XPATH, '//*[@id="radix-:R3i99uutpuu4q:"]/button')
        skills_section_close_button.click()

        tasks_section_header = driver.find_element(By.XPATH, '//*[@id="sticky-tabs"]/div[2]/button[3]')
        tasks_section_header.click()

        tasks_container = driver.find_element(By.XPATH, '//*[@id="tasks-section"]/div/div[1]')

        task_buttons = tasks_container.find_elements(By.TAG_NAME, 'button')
        for task_button in task_buttons:
            action.move_to_element(task_button).perform()
            task_button.click()
            task_title = task_button.find_element(By.CSS_SELECTOR, 'span.w-full').text
            task_content_container = driver.find_element(By.XPATH, "//*[@class='flex items-start justify-start w-full py-8 px-6 gap-4 flex-col h-fit']")

            print(task_content_container.text)
            break









    
    except TimeoutException:
        print("Page load timed out")
        return None


scrape_one_url('https://www.theforage.com/simulations/commonwealth-bank/intro-cybersecurity-rdxl')

# def scrape_example(url):
#     driver = create_driver(headless=False)

#     try:
#         driver.get(url)

#         wait = WebDriverWait(driver, 15)

#         # Wait for page body to load
#         wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

#         # Example: extract page title
#         title = driver.title

#         # Example: extract all links
#         links = driver.find_elements(By.TAG_NAME, "a")
#         extracted_links = [link.get_attribute("href") for link in links if link.get_attribute("href")]

#         return {
#             "title": title,
#             "links": extracted_links
#         }

#     except TimeoutException:
#         print("Page load timed out")
#         return None

#     finally:
#         driver.quit()


# if __name__ == "__main__":
#     url = "https://example.com"
#     data = scrape_example(url)

#     if data:
#         print("Title:", data["title"])
#         print("Found", len(data["links"]), "links")
