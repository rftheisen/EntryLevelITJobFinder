from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
import time

def scrape_jobs(location):
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
    driver.get(f"https://www.indeed.com/jobs?q=entry+level+IT&l={location}")
    time.sleep(5)  # Wait for the page to load fully

    job_list = []

    try:
        # Wait for job cards to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'job_seen_beacon'))  # Updated class name
        )

        jobs = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')
        for job in jobs:
            try:
                # Use different strategies to locate elements
                
                # Job Title
                try:
                    title_element = job.find_element(By.CSS_SELECTOR, 'h2.jobTitle > a')
                    title = title_element.text if title_element else "No title provided"
                except:
                    title = "No title provided"
                
                # Company Name
                try:
                    company_element = job.find_element(By.CSS_SELECTOR, 'span.companyName')
                    company = company_element.text.strip() if company_element else "No company provided"
                except:
                    company = "No company provided"

                # Location
                try:
                    location_element = job.find_element(By.CSS_SELECTOR, 'div.companyLocation')
                    job_location = location_element.text.strip() if location_element else "No location provided"
                except:
                    job_location = "No location provided"

                # Summary
                try:
                    summary_element = job.find_element(By.CSS_SELECTOR, 'div.job-snippet')
                    summary = summary_element.text.strip() if summary_element else "No summary provided"
                except:
                    summary = "No summary provided"

                # Link
                link = title_element.get_attribute('href') if title_element else "No link available"

                job_list.append({
                    "title": title,
                    "company": company,
                    "location": job_location,
                    "summary": summary,
                    "link": link
                })

                # Debug print statements to see if data is being collected correctly
                print(f"Job Title: {title}")
                print(f"Company: {company}")
                print(f"Location: {job_location}")
                print(f"Summary: {summary}")
                print(f"Link: {link}\n")

            except Exception as e:
                print(f"Error scraping a job element: {e}")

    except Exception as e:
        print(f"Error waiting for job elements: {e}")

    finally:
        driver.quit()

    return job_list

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gogetjobs.py <location>")
        sys.exit(1)

    location = sys.argv[1]
    jobs = scrape_jobs(location)

    if jobs:
        print(f"Found {len(jobs)} jobs.")
        with open('jobs.json', 'w') as json_file:
            json.dump(jobs, json_file, indent=4)
    else:
        print("No jobs found.")
