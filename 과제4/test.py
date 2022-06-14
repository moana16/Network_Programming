import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


def scrapping():
    url = 'https://sites.google.com/view/davidchoi/home/members'
    page = requests.get(url)
    soup = bs(page.text, "html.parser")
    elements = soup.select_one(
        '#yDmH0d > div:nth-child(1) > div > div:nth-child(2) > div.QZ3zWd > div > div.UtePc.RCETm.SwuGbc')
    # select img tag
    imgs = elements.select('section > div > div > div > div > div > div > div > div > div > div > img')
    # select description
    titles = elements.select('section > div > div > div > div > div > div > div > div > div > p')
    dataList = []

    # for image index number
    index = 0
    # in for loop if name_flag is False, save as name data
    # if name_flag is True, save as research data
    name_flag = False

    for title in titles:
        if title.text == '':
            continue

        if name_flag == False:
            name = title.text.split('(')[0]
            role_year = title.text.split('(')[1].split(')')[0]
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
                research_interest = title.text.split(':')[1]
                if research_interest == '' or research_interest == ' ':
                    research_interest = 'NA'
            except IndexError:
                research_interest = title.text

            # select picture url by index
            profile_pic_url = imgs[index]['src']
            if profile_pic_url == '' or profile_pic_url == ' ':
                profile_pic_url = 'NA'

            data = [name, job_role, start_year, end_year, research_interest, profile_pic_url]
            dataList.append(data)
            name_flag = False
            index += 1
            continue

            # make list to dataframe
    df = pd.DataFrame(dataList,
                      columns=['name', 'job_role', 'start_year', 'end_year', 'interest_role', 'profile_pic_url'])
    print(df)
    # make dataframe to csv file
    df.to_csv('./problem2_csv.csv', mode='w')


if __name__ == '__main__':
    print('Trying to scrap data...')
    scrapping()
    print('Data saved! Check \'problem2_csv.csv\' file!')