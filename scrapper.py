from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


# Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = "https://www.naukri.com/full-stack-developer-jobs-in-pune"
driver.get(url)


time.sleep(5)


data = []


# Loop through multiple pages
while True:
    time.sleep(3)  # wait for jobs to load


    jobs = driver.find_elements(By.CSS_SELECTOR, "div.cust-job-tuple.layout-wrapper.lay-2.sjw__tuple")


    for job in jobs:
        try:
            # Title & Link
            a_tag = job.find_element(By.CSS_SELECTOR, "a.title")
            title = a_tag.text.strip()
            link = a_tag.get_attribute("href")


            # Company Name
            try:
                company_tag = job.find_element(By.CSS_SELECTOR, "a.comp-name")
                company = company_tag.text.strip()
            except:
                company = "N/A"


            data.append({"title": title, "link": link, "company": company})
        except:
            continue


    # Try to go to next page
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "a.fright.fs14.btn-secondary.br2")  # Next button
        if "disabled" in next_button.get_attribute("class"):  # no more pages
            break
        else:
            next_button.click()
            time.sleep(3)
    except:
        break


driver.quit()


# Save to CSV
with open("naukri_jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "company", "link"])
    writer.writeheader()
    writer.writerows(data)


print(f"✅ Saved {len(data)} jobs to naukri_jobs.csv")