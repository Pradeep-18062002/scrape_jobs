import requests
from bs4 import BeautifulSoup
from utils import is_within_time
from datetime import datetime

def get_total_pages(soup) -> int:
    pagination_buttons = soup.select("button.pagination-button")
    page_numbers = [
        int(button.get_text(strip=True))
        for button in pagination_buttons
        if button.get_text(strip=True).isdigit()
    ]
    return max(page_numbers) if page_numbers else 1

def get_college_sports_jobs(given_date:int):
    base_url = "https://collegesports.jobs/jobs?page={}"
    scraped_jobs = []

    try:
        first_page = requests.get(base_url.format(1))
        first_page.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch page 1: {e}")
        return scraped_jobs

    soup = BeautifulSoup(first_page.text, "html.parser")
    total_pages = get_total_pages(soup)

    for page_num in range(1, total_pages + 1):
        try:
            res = requests.get(base_url.format(page_num))
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
        except requests.RequestException as e:
            print(f"Failed to fetch page {page_num}: {e}")
            continue

        job_cards = soup.select("div.job-postings-item__main")

        for job in job_cards:
            try:
                # Initialize variables
                posted_dt = None
                formatted_date = None
                title = None
                full_link = None
                company = None
                address = None

                # Extract date
                time_tag = job.select_one("time.job-postings-item__date")
                if time_tag:
                    raw_date_text = time_tag.get_text(strip=True)
                    posted_dt = datetime.strptime(raw_date_text, "%B %d, %Y")
                    formatted_date = posted_dt.strftime("%m/%d/%y")

                # Extract job title and link
                job_title_tag = job.select_one("h3 a.job-postings-item__title")
                if job_title_tag:
                    title = job_title_tag.get_text(strip=True)
                    relative_link = job_title_tag.get("href")
                    full_link = f"https://collegesports.jobs{relative_link}"

                # Extract company and address
                company_tag = job.select_one("span.job-postings-item__employer")
                company = company_tag.get_text(strip=True) if company_tag else None

                address_tag = job.select_one("span.job-postings-item__address")
                address = address_tag.get_text(strip=True) if address_tag else None

                # Time filter
                if posted_dt and is_within_time(posted_dt.strftime("%m/%d/%y"), given_date):
                    scraped_jobs.append({
                        "title": title,
                        "company": company,
                        "region": address,
                        "link": full_link,
                        "posted": formatted_date
                    })

            except Exception as e:
                print(f"Error parsing job: {e}")

    return scraped_jobs