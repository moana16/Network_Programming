import pandas as pd
import requests
from bs4 import BeautifulSoup 


url = 'https://sites.google.com/view/davidchoi/home/members'
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
tags = soup.select_one(
    '#yDmH0d > div:nth-child(1) > div > div:nth-child(2) > div.QZ3zWd > div > div.UtePc.RCETm.SwuGbc')

imgs = tags.select('section > div > div > div > div > div > div > div > div > div > div > img')

lists = tags.select('section > div > div > div > div > div > div > div > div > div > p')
dataList = []

# for image index number
i = 0
# in for loop if name_flag is False, save as name data
# if name_flag is True, save as research data
name_flag = False

for list in lists:
    if list.text == '':
        continue

    if name_flag == False:
        name = list.text.split('(')[0]
        role_year = list.text.split('(')[1].split(')')[0]
        job_role = role_year.split(',')[0]
        start_year = role_year.split(',')[1].split('-')[0]
        try:
            end_year = role_year.split(',')[1].split('-')[1]
            if end_year == '':
                end_year = 'NA'
        except IndexError:
            end_year = start_year
        name_flag = True
        continue
    else:
        try:
            research_interest = list.text.split(':')[1]
            if research_interest == '' or research_interest == ' ':
                research_interest = 'NA'
        except IndexError:
            research_interest = list.text

        
        profile_pic_url = imgs[i]['src']
        if profile_pic_url == '' or profile_pic_url == ' ':
            profile_pic_url = 'NA'

        data = [name, job_role, start_year, end_year, research_interest, profile_pic_url]
        dataList.append(data)
        name_flag = False
        i += 1
        continue


df = pd.DataFrame(dataList,
                    columns=['name', 'job_role', 'start_year', 'end_year', 'interest_role', 'profile_pic_url'])


df.to_csv('./problem2_csv.csv', mode='w')