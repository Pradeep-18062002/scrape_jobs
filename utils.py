from datetime import datetime

VALID_USA_REGIONS = [
    "Northeast Region", "Southeast Region", "Central Region", "West Region", "Nationwide"
]

def is_within_time(posted_str: str, days: int) -> bool:
    try:
        post_date = datetime.strptime(posted_str.strip(), "%m/%d/%y")
        return (datetime.now() - post_date).days < days
    except Exception:
        return "today" in posted_str.lower() or "hour" in posted_str.lower()