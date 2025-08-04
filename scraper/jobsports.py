import requests
from bs4 import BeautifulSoup
import re
from utils import VALID_USA_REGIONS , is_within_time


def get_total_pages(soup)->int:
    pagination_links = soup.select("a")
    page_numbers=[]

    for link in pagination_links:
        href = link.get("href")
        if href:
            match = re.search(r"p=(\d+)",href)
            if match:
                page_numbers.append(int(match.group(1)))
    return max(set(page_numbers)) if page_numbers else 1

def fetch_jobsinsports(given_date:int):
    base_url = "https://www.jobsinsports.com/Content/Members/index_public.cfm?p={}&myJobs=0&matchingJobs=0&company="
    scraped_jobs = []

    first_page = requests.get(base_url.format(1))
    soup = BeautifulSoup(first_page.text,"html.parser")
    total_pages = get_total_pages(soup)

    for page_num in range(1, total_pages+1):
        res = requests.get(base_url.format(page_num))
        soup = BeautifulSoup(res.text,"html.parser")
        job_cards = soup.select("div.row.search_results, div.row.search_results.premium_listing")

        for card in job_cards:
            
            try:
                title_elem = card.select_one("h4 a")
                title = title_elem.get_text(strip=True)
                link = title_elem.get("href")
                link = f"https://www.jobsinsports.com{link}" if link else ""

                date_label = card.find(string = re.compile("Posted/Updated:"))
                date_str = date_label.split(":")[-1].strip() if date_label else ""
                job_attrs = card.select("div.job_attribute")
                company = job_attrs[0].get_text(strip=True) if len(job_attrs) > 0 else ""
                region = job_attrs[1].get_text(strip=True) if len(job_attrs) > 1 else ""


                if region in VALID_USA_REGIONS and is_within_time(date_str, given_date):
                    scraped_jobs.append({
                        "title": title,
                        "company": company,
                        "region": region,
                        "link": link,
                        "posted": date_str
                    })

            except Exception as e:
                print(f"Skipping one job due to error: {e}")
                continue
    return scraped_jobs