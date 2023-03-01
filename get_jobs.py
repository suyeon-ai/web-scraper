from indeed import get_jobs as get_indeed_jobs
from flexjobs import get_jobs as get_flexjobs_jobs
#from save import save_to_file

def get_jobs (word):
  indeed_jobs = get_indeed_jobs(word)
  Flexjobs_jobs = get_flexjobs_jobs(word)
  
  jobs = indeed_jobs + Flexjobs_jobs
  return jobs
#save_to_file(jobs)