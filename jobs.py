from bs4 import BeautifulSoup
import requests
import time
#request a link that have our data
def recent_jobs(page_number=0,counter=0,job_text=""):# this program gets recent jobs on wuzzuf website
    page=requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=&start={page_number}").text
    #using beautiful soup to get readable html
    soup=BeautifulSoup(page,'lxml')
    #find jobs in soup
    jobs=soup.find_all('div',class_="css-pkv5jc")
    for job in jobs:
        counter+=1 #job number
        job_title=job.find('h2',class_="css-m604qf").a#job title element
        company_name=job.find('a',class_="css-17s97q8")#company name element
        company_location=job.find('span',class_="css-5wys0k").text#company location text
        added_in=job.find('div',class_="css-4c4ojb").text#the addition day text
        if 'days' in added_in:# if not recent end the program
            with open("jobs.txt",'w') as file:
                file.write(job_text)
            return 0
        Type=job.find('span',class_='css-1ve4b75').text# job type text
        sblock=job.find('div',class_='css-y4udm8')# skills block
        skills_list=sblock.find_all('a',class_='css-o171kl')
        skills_list.extend(sblock.find_all('a',class_='css-5x9pm1'))
        skills_list.insert(1,sblock.find_all('span')[1])
        skills=""
        for skill in skills_list:
            skills+=skill.text# job skills
        job_text+=f"({counter}) Job title: {job_title.text}.\n    for more info: https://wuzzuf.net/{job_title['href']}.\n"
        try:
            job_text+=f"    Company name: {company_name.text}.\n    for more info about company: {company_name['href']}.\n"
        except:
            job_text+=f"    Company name: Confidential.\n"
        job_text+=f"    Company location: {company_location}.\n"
        job_text+=f"    Job type: {Type}.\n"
        job_text+=f"    Required skills: {skills}.\n"
        job_text+="\n"
    page_number+=1
    recent_jobs(page_number,counter,job_text)
if __name__=="__main__":#start app
    while True:
        recent_jobs()
        waiting=10
        print(f"Waiting for {waiting} minutes...")
        time.sleep(waiting*60)