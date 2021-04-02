#!/usr/bin/env python
# coding: utf-8




import requests
from bs4 import BeautifulSoup
import time
from requests import get
import pandas as pd
import io
import os.path


#Searching IT jobs in Lisboa


URL = "https://www.itjobs.pt/emprego?location=14"
page= requests.get(URL)

soup= BeautifulSoup(page.content, 'html.parser')





#checking first 10 pages of listed jobs
num_pages=10

name_of_jobs=[]
name_of_companies=[]
loctime_details=[]

for i in range (1,num_pages):   
    
    time.sleep(30) #give enough time between page loads to avoid server overload
    print(f"Reading page {i}")
    
    list_page_url=f"{URL}&page{i}"
    list_page=requests.get(list_page_url)
    list_soup=BeautifulSoup(list_page.content, "html.parser")

    job_names=soup.find_all("a",class_="title")
    job_companies=soup.find_all("div",class_="list-name")
    job_details=soup.find_all("div",class_="list-details")

    for jobs in job_names:
        name_of_jobs.append(jobs.text.strip())

    for company in job_companies:
        name_of_companies.append(company.text.strip())

    for details in job_details:
        loctime_details.append(details.text.strip())
    





#Building dataframe with job information: name, company and location with part/full time

name_of_jobs_df=pd.DataFrame(name_of_jobs)
name_of_companies_df=pd.DataFrame(name_of_companies)
loctime_details_df=pd.DataFrame(loctime_details)

jobs_info=pd.concat([name_of_jobs_df,name_of_companies_df,loctime_details_df],axis=1)

jobs_info.columns=["Job name","Company","Location and Full/Part"]

jobs_info.head()





# Profile report: quick summary to check number of job names and job companies -  see if there are more common jobs or a company with more job openings.

import pandas_profiling as  pp
jobs_info_clean=jobs_info.dropna()


PR_IT = pp.ProfileReport(jobs_info_clean, minimal=True)

jobs_info_clean.to_csv("./jobs_IT.csv")

PR_IT.to_file(output_file="summaryReport_IT_jobs.html")




