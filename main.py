from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from scraper.jobsports import fetch_jobsinsports 
from scraper.collegesportsjobs import get_college_sports_jobs
from scraper.teamworkonline import get_team_work_online_jobs
app = FastAPI()


def jobsinsports(days):
    jobs = fetch_jobsinsports(days)
    return jobs

def college_sports_jobs(days):
    jobs = get_college_sports_jobs(days)
    return jobs

def team_work_online_jobs(days):
    jobs = get_team_work_online_jobs(days)
    return jobs

@app.get("/jobs")
def scrape_jobs(days_for_jobsinsports: int = Query(..., ge=1,le = 60),days_for_college_sports_jobs: int = Query(..., ge=1,le = 60), days_for_teamworkonline: int = Query(..., ge=1,le = 90)):
    
    res1 = jobsinsports(days_for_jobsinsports)
    res2 = college_sports_jobs(days_for_college_sports_jobs)
    res3 = team_work_online_jobs(days_for_teamworkonline)
    
    return JSONResponse(content={
        "jobsinsports": res1,
        "collegesportsjobs": res2,
        "teamworkonline": res3
    })