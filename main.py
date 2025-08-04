from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from scraper.jobsports import fetch_jobsinsports 
from scraper.collegesportsjobs import get_college_sports_jobs
from scraper.teamworkonline import get_team_work_online_jobs
app = FastAPI()

@app.get("/jobsinsports")
def jobsinsports_endpoint(days: int = Query(..., ge=1,le = 60)):
    jobs = fetch_jobsinsports(days)
    return JSONResponse(content={"jobs": jobs})

@app.get("/collegesportsjobs")
def college_sports_jobs_endpoint(days: int = Query(...,ge=1,le = 60)):
    jobs = get_college_sports_jobs(days)
    return JSONResponse(content={"jobs": jobs})

@app.get("/teamworkonlinejobs")
def team_work_online_jobs(days: int = Query(..., ge=1, le=90)):
    jobs = get_team_work_online_jobs(days)
    return JSONResponse(content={"jobs": jobs})


    