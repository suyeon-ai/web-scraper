import requests
from bs4 import BeautifulSoup


def extract_last_page(URL):
  page = 1
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("ul", {"class":"pagination"}).find_all('a')
  last_page = int(pagination[-2].get_text())
  return last_page


def extract_jobs_detail(html):
  title = html.find('a').get_text()
  company = "Check after logging in after login"
  location = html.find("div", {"class":"job-locations"}).get_text().strip()
  job_id = html.find('a')["href"]
  return {
    "title":title, 
    "company":company, 
    "location":location, 
    "link":f"https://www.flexjobs.com{job_id}"}


def extract_jobs(last_page, URL):
  jobs_detail = []
  for page in range(last_page)[0:1]:
    print(f"Scrapping flexjobs page {page}")
    result = requests.get(f"{URL}&page={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    result_contents = soup.find_all("div",{"class":"col-md-12 col-12"})
    for html in result_contents:
      job = extract_jobs_detail(html)
      jobs_detail.append(job)
  return jobs_detail 


def get_jobs(word):
  URL = f"https://www.flexjobs.com/search?location=&search={word}"
  last_page = extract_last_page(URL)
  jobs = extract_jobs(last_page, URL)
  return jobs