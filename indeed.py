import requests
from bs4 import BeautifulSoup

limit = 50

#만약 limit 값을 알 수 없었다면,
'''def extract_limit():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  each_page_jobs_count = int(soup.find("link",{"rel":"next"})["href"].split("&start=")[-1])
  limit = each_page_jobs_count
  return limit'''

  
def extract_last_page(URL):
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  total_jobs_count = soup.find("div", {"id":"searchCountPages"}).string.strip().split(" ")
  last_page = int(int(total_jobs_count[-1].strip('건').replace(',','')) / limit)
  return last_page


def extract_jobs_detail(html):
  title = html.find('a').find("span")["title"]
  company = html.find("div", {"class":"companyInfo"}).find("span").string
  location = html.find("div", {"class":"companyLocation"}).string
  job_id = html.find('a')["data-jk"]
  return {
    "title":title, 
    "company":company, 
    "location":location, 
    "link":f"https://kr.indeed.com/viewjob?jk={job_id}"}


def extract_jobs(last_page, URL):
  jobs_detail = []
  for page in range(last_page)[0:1]:
    print(f"Scrapping indeed page {page}")
    result = requests.get(f"{URL}&start={page*limit}")
    soup = BeautifulSoup(result.text, "html.parser")
    result_contents = soup.find_all("td",{"class":"resultContent"})
    for html in result_contents:
      job = extract_jobs_detail(html)
      jobs_detail.append(job)
  return jobs_detail 


def get_jobs(word):
  URL = f"https://kr.indeed.com/jobs?q={word}&limit={limit}"
  last_page = extract_last_page(URL)
  jobs = extract_jobs(last_page, URL)
  return jobs