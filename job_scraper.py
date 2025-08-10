import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_indeed(role, location=""):
    """Scrape Indeed job listings for a given role and optional location."""
    role_query = role.replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={role_query}&l={location}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_list = []
    for job_card in soup.find_all("div", class_="job_seen_beacon"):
        title_elem = job_card.find("h2", class_="jobTitle")
        company_elem = job_card.find("span", class_="companyName")
        location_elem = job_card.find("div", class_="companyLocation")
        link_elem = job_card.find("a")

        if title_elem and link_elem:
            job_url = "https://www.indeed.com" + link_elem["href"]
            job_desc = get_job_description(job_url)
            job_list.append({
                "title": title_elem.text.strip(),
                "company": company_elem.text.strip() if company_elem else "",
                "location": location_elem.text.strip() if location_elem else "",
                "description": job_desc
            })
            time.sleep(1)  # Be polite to the server
    return job_list

def get_job_description(url):
    """Visit the job posting and extract full description."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    desc_elem = soup.find("div", class_="jobsearch-jobDescriptionText")
    return desc_elem.get_text(separator="\n").strip() if desc_elem else ""

if __name__ == "__main__":
    roles = [
        "Python Developer",
        "Data Scientist",
        "Web Developer",
        "Machine Learning Engineer"
    ]
    all_jobs = []

    for role in roles:
        print(f"Scraping jobs for: {role}")
        jobs = scrape_indeed(role)
        all_jobs.extend(jobs)

    with open("job_descriptions.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=4, ensure_ascii=False)

    print(f"✅ Saved {len(all_jobs)} job descriptions to job_descriptions.json")
