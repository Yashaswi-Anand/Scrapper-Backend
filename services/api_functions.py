from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

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


def get_simple_data(tech_job: str, location: str):
    return {
  "message": "Scraped 20 jobs from Naukri.com",
  "data": [ 
    {
      "title": "Python Software Developer-AB-Bengaluru, Hyd",
      "link": "https://www.naukri.com/job-listings-python-software-developer-ab-bengaluru-hyd-infosys-kolkata-bengaluru-delhi-ncr-3-to-8-years-240125016513",
      "company": "Infosys"
    },
    {
      "title": "Python Software Developer & Infosys- Pan India",
      "link": "https://www.naukri.com/job-listings-python-software-developer-infosys-pan-india-infosys-pune-delhi-ncr-mumbai-all-areas-3-to-8-years-140825015440",
      "company": "Infosys"
    },
    {
      "title": "Python Developer @ Infosys- Pan India",
      "link": "https://www.naukri.com/job-listings-python-developer-infosys-pan-india-infosys-pune-delhi-ncr-mumbai-all-areas-4-to-9-years-100625011129",
      "company": "Infosys"
    },
    {
      "title": "Python Software Developer & Infosys- Pan India(F)",
      "link": "https://www.naukri.com/job-listings-python-software-developer-infosys-pan-india-f-infosys-pune-delhi-ncr-mumbai-all-areas-3-to-8-years-140825015534",
      "company": "Infosys"
    },
    {
      "title": "Python Software Developer",
      "link": "https://www.naukri.com/job-listings-python-software-developer-amity-software-systems-delhi-ncr-5-to-10-years-120825027559",
      "company": "Amity Software Systems"
    },
    {
      "title": "Python Developer",
      "link": "https://www.naukri.com/job-listings-python-developer-trigyn-technologies-new-delhi-3-to-5-years-080825503471",
      "company": "Trigyn Technologies"
    },
    {
      "title": "Remote Python Developer 38 Lakhs CTC || Kandi Srinivasa",
      "link": "https://www.naukri.com/job-listings-remote-python-developer-38-lakhs-ctc-kandi-srinivasa-vcloud-technologies-investment-kolkata-bengaluru-delhi-ncr-9-to-14-years-290325004572",
      "company": "Integra Technologies"
    },
    {
      "title": "Python Developer",
      "link": "https://www.naukri.com/job-listings-python-developer-perfios-software-solutions-bengaluru-delhi-ncr-mumbai-all-areas-1-to-6-years-170325000069",
      "company": "Perfios Software Solutions"
    },
    {
      "title": "Python Software Developer- Pune",
      "link": "https://www.naukri.com/job-listings-python-software-developer-pune-infosys-pune-delhi-ncr-mumbai-all-areas-5-to-10-years-200825036111",
      "company": "Infosys"
    },
    {
      "title": "Python Developer",
      "link": "https://www.naukri.com/job-listings-python-developer-appzlogic-mobility-solutions-pvt-ltd-kolkata-mumbai-new-delhi-hyderabad-pune-chennai-bengaluru-0-to-3-years-121124502854",
      "company": "Appzlogic"
    },
    {
      "title": "Python Developer",
      "link": "https://www.naukri.com/job-listings-python-developer-legitquest-new-delhi-1-to-6-years-110825502592",
      "company": "Legitquest"
    },
    {
      "title": "Python Web developer",
      "link": "https://www.naukri.com/job-listings-python-web-developer-trigyn-technologies-new-delhi-3-to-7-years-070125020444",
      "company": "Trigyn Technologies"
    },
    {
      "title": "Python Software Developer",
      "link": "https://www.naukri.com/job-listings-python-software-developer-fyora-ai-new-delhi-1-to-3-years-050825027770",
      "company": "Fyora.ai"
    },
    {
      "title": "Developer (Python)",
      "link": "https://www.naukri.com/job-listings-developer-python-contata-solutions-pvt-ltd-new-delhi-3-to-5-years-180825503254",
      "company": "Contata Solutions"
    },
    {
      "title": "Python Developer",
      "link": "https://www.naukri.com/job-listings-python-developer-taxmann-delhi-ncr-1-to-2-years-140825931674",
      "company": "Taxmann Publications"
    },
    {
      "title": "Python Developer",
      "link": "https://www.naukri.com/job-listings-python-developer-response-informatics-kolkata-mumbai-new-delhi-hyderabad-pune-chennai-bengaluru-6-to-8-years-110825502198",
      "company": "Response Informatics"
    },
    {
      "title": "Python Developer - Senior Software",
      "link": "https://www.naukri.com/job-listings-python-developer-senior-software-xerox-business-solutions-southeast-kolkata-mumbai-new-delhi-hyderabad-pune-chennai-bengaluru-3-to-6-years-030425502179",
      "company": "Xerox Business Solutions Southeast"
    },
    {
      "title": "Python Developer",
      "link": "https://www.naukri.com/job-listings-python-developer-aark-global-inc-kolkata-mumbai-new-delhi-hyderabad-pune-chennai-bengaluru-5-to-10-years-190825500726",
      "company": "Aark Global"
    },
    {
      "title": "Python Software Developer",
      "link": "https://www.naukri.com/job-listings-python-software-developer-cloudxtreme-bengaluru-delhi-ncr-mumbai-all-areas-4-to-9-years-130825004010",
      "company": "Cloudxtreme"
    },
    {
      "title": "Python Developer",
      "link": "https://www.naukri.com/job-listings-python-developer-bytespoke-arrixa-kolkata-mumbai-new-delhi-hyderabad-pune-chennai-bengaluru-9-to-14-years-120825500157",
      "company": "Bytespoke Com"
    }
  ]
}