import requests
from bs4 import BeautifulSoup
import pandas as pd
from pick import pick

def google_parse(keyword, user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"):
    keyword = keyword.replace(' ', '+')
    URL = f"https://google.com/search?q={keyword}"
    headers = {"user-agent": user_agent}
    resp = requests.get(URL, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        links = []
        for g in soup.find_all('div', class_='g'):
            element = g.find('div', class_='jtfYYd')
            if element:
                divs = element.find_all('div', recursive=False)
                if len(divs) >= 2:
                    anchor = divs[0].find('a')
                    link = anchor['href']
                    links.append(link)
        return links


def links_parse(links):
    count = 1
    items = []
    title = ''
    description = ''
    for link in links:
        resp = requests.get(link)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            head = soup.html.find("head", recursive=False)
            if head.find("title"):
                title = head.find("title").text
            if head.find(attrs={"name": "description"}):
                description = head.find(attrs={"name": "description"})
            item = {
                'position': count,
                'link': link,
                'title': title,
                'description': description
            }
            title = ''
            description = ''
            items.append(item)
            count += 1
    return items

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

# Input keyword and search type
keyword = input('Input your keyword: ')
title = 'Desktop or Mobile: '
options = ['Desktop', 'Mobile']
option, index = pick(options, title)

if option == 'Desktop':
    user_agent = USER_AGENT
else:
    user_agent = MOBILE_USER_AGENT

links = google_parse(keyword)

# Convert to xlsx
z = pd.DataFrame(links_parse(links))
z.to_excel(f"{keyword}_{option}.xlsx", index=False)

print(f'Ready! {keyword}_{option}.xlsx has been created')
