from selenium import webdriver                       # Selenium main WebDriver API
from selenium.webdriver.common.by import By          # Locator strategies (By.CSS_SELECTOR, By.XPATH, etc.)
from selenium.webdriver.chrome.service import Service # To start ChromeDriver cleanly
from webdriver_manager.chrome import ChromeDriverManager # Auto-download the right ChromeDriver
import time                                          # Simple (crude) waits
import csv                                           # Write rows to a CSV file

# ---- Browser setup ----
options = webdriver.ChromeOptions()                  # Create a Chrome options object
options.add_argument("--start-maximized")           # Open the browser window maximized (helps when elements are off-screen)
options.add_argument("--disable-blink-features=AutomationControlled")  # Slightly reduces bot detection

# Start Chrome with the managed driver and options
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

url = "https://www.naukri.com/full-stack-developer-jobs-in-pune"  # Target page
driver.get(url)                                   # Navigate the browser to the URL

time.sleep(5)                                     # Give the page time to render and load JS content (basic wait)

data = []                                         # This list will hold dicts like {"title": ..., "company": ..., "link": ...}

# ---- Pagination loop: keep scraping until we can't find/click 'Next' ----
while True:
    time.sleep(3)                                  # Small wait on each page for job cards to render

    # Grab all job cards on the current page by their combined classes
    jobs = driver.find_elements(
        By.CSS_SELECTOR, 
        "div.cust-job-tuple.layout-wrapper.lay-2.sjw__tuple"
    )

    # Iterate over each job card and extract fields
    for job in jobs:
        try:
            # Title & link are inside <a class="title"> within the card
            a_tag = job.find_element(By.CSS_SELECTOR, "a.title")
            title = a_tag.text.strip()            # Visible text inside the <a>
            link = a_tag.get_attribute("href")    # Destination URL of the job

            # Company name is inside <a class="comp-name"> (usually under .row2)
            try:
                company_tag = job.find_element(By.CSS_SELECTOR, "a.comp-name")
                company = company_tag.text.strip()
            except:
                company = "N/A"                   # If not found, fall back gracefully

            # Store this row as a dict
            data.append({"title": title, "link": link, "company": company})

        except:
            # If this card is malformed or selectors change, skip it
            continue

    # ---- Try to move to the next results page ----
    try:
        # The 'Next' button typically has these classes; adjust if Naukri changes UI
        next_button = driver.find_element(
            By.CSS_SELECTOR, 
            "a.fright.fs14.btn-secondary.br2"
        )
        # If the button is disabled (end of pages), stop
        if "disabled" in next_button.get_attribute("class"):
            break
        else:
            next_button.click()                   # Go to the next page
            time.sleep(3)                         # Wait for navigation + render
    except:
        # If 'Next' isn't present, we're done
        break

driver.quit()                                      # Close the browser session

# ---- Write everything to CSV ----
with open("naukri_jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "company", "link"])
    writer.writeheader()                           # First row: column names
    writer.writerows(data)                         # One row per job

print(f"✅ Saved {len(data)} jobs to naukri_jobs.csv")