from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def get_driver():
    options = Options()
    options.add_argument("--headless=new")   # Headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(
        executable_path="/usr/bin/chromedriver",
        options=options
    )
    return driver

def get_latest_job_data(tech_job: str, location: str):
    """
    Scrapes job data from Naukri.com and returns it as a JSON response.
    """
    # ---- Browser setup ----
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Start Chrome with the managed driver and options
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    url = f"https://www.naukri.com/{tech_job}-jobs-in-{location}"
    driver.get(url)

    time.sleep(5)

    data = []

    # ---- Pagination loop: keep scraping until we can't find/click 'Next' ----
    while True:
        time.sleep(3)

        jobs = driver.find_elements(
            By.CSS_SELECTOR,
            "div.cust-job-tuple.layout-wrapper.lay-2.sjw__tuple"
        )

        for job in jobs:
            try:
                a_tag = job.find_element(By.CSS_SELECTOR, "a.title")
                title = a_tag.text.strip()
                link = a_tag.get_attribute("href")

                try:
                    company_tag = job.find_element(By.CSS_SELECTOR, "a.comp-name")
                    company = company_tag.text.strip()
                except:
                    company = "N/A"

                data.append({"title": title, "link": link, "company": company})

            except:
                continue

        # ---- Try to move to the next results page ----
        try:
            next_button = driver.find_element(
                By.CSS_SELECTOR,
                "a.fright.fs14.btn-secondary.br2"
            )
            if "disabled" in next_button.get_attribute("class"):
                break
            else:
                next_button.click()
                time.sleep(3)
        except:
            break

    driver.quit()

    return {"message": f"Scraped {len(data)} jobs from Naukri.com", "data": data}