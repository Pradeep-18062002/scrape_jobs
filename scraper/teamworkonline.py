import requests
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
from dateutil.relativedelta import relativedelta

def get_total_pages(soup)->int:
  page_numbers=[]
  page_spans = soup.select("nav.pagination span.page")

  for span in page_spans:
    if span.string and span.string.strip().isdigit():
      page_numbers.append(int(span.string.strip()))
    elif span.a and span.a.text.strip().isdigit():
      page_numbers.append(int(span.a.text.strip()))
  return max(page_numbers) if page_numbers else 1


def get_team_work_online_jobs(filter_days:int):
  base_url = "https://www.teamworkonline.com/jobs-in-sports?page={}"
  scraped_jobs=[]
  today = datetime.now()
  cutoff_date = today  - timedelta(days = filter_days)


  try:
    first_page = requests.get(base_url.format(1))
    first_page.raise_for_status()
  except requests.RequestException as e:
    print(f"Failed to fetch page 1: {e}")
    return scraped_jobs
  soup = BeautifulSoup(first_page.text,"html.parser")
  total_pages = get_total_pages(soup)
  stop_scraping = False

  for page in range(1,total_pages+1):
    try:
      response = requests.get(base_url.format(page))
      response.raise_for_status()
      soup = BeautifulSoup(response.text,"html.parser")
    except requests.RequestException as e:
      print(f"Failed to fetch page {page}: {e}")
      break
  
  
    job_cards = soup.select("div.browse-jobs-card div.browse-jobs-card__content")

    for card in job_cards:
      try:
        time_date= card.select("div.browse-jobs-card__scoreboard")
        time=""
        for time_digit in time_date:
          digit = time_digit.getText(strip=True)
          time+=digit
        if '+' in time:
          continue
        try:
          time = int(time)
        except ValueError:
          time=None 
        unit_tag = card.select_one("div.trending__scoreboard--time")
        unit = unit_tag.get_text(strip = True).lower() if unit_tag else ""

        

        if time is not None:
          if "day" in unit:
            posted_date = today - timedelta(days=time)
          elif "hour" in unit:
            posted_date = today - timedelta(hours=time)
          elif "month" in unit:
            posted_date = today - relativedelta(months=time)
          else:
            continue

          if posted_date <cutoff_date:
            return scraped_jobs
          
          posted_time = f"{time} {unit}"
          relative_link_tag = card.select_one("a.browse-jobs-card__content--title")
          relative_link = relative_link_tag.get("href").strip()
          base_link = "https://www.teamworkonline.com"
          job_link = base_link+relative_link
          title_tag = relative_link_tag.select_one("div.margin-none")
          job_title= title_tag.get_text(strip= True)
          company_tag = card.select_one("div.browse-jobs-card__content--organization")
          job_company= company_tag.get_text(strip=True)
          location_tag = card.select_one("div.trending__content--small")
          job_location = location_tag.get_text(strip = True)

          scraped_jobs.append({
                          "title": job_title,
                          "company": job_company,
                          "location": job_location,
                          "posted_time": posted_time,
                          "posted_date": posted_date.strftime("%B %d, %Y"),
                          "link": job_link,
                      })
          
      except Exception as e:
                  print(f"Error parsing job card: {e}")
                  continue
  return scraped_jobs
