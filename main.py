from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


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


def scrape_example(url):
    driver = create_driver(headless=False)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        # Wait for page body to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Example: extract page title
        title = driver.title

        # Example: extract all links
        links = driver.find_elements(By.TAG_NAME, "a")
        extracted_links = [link.get_attribute("href") for link in links if link.get_attribute("href")]

        return {
            "title": title,
            "links": extracted_links
        }

    except TimeoutException:
        print("Page load timed out")
        return None

    finally:
        driver.quit()


if __name__ == "__main__":
    url = "https://example.com"
    data = scrape_example(url)

    if data:
        print("Title:", data["title"])
        print("Found", len(data["links"]), "links")
