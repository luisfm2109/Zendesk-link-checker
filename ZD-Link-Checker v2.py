import requests, json, re, time
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd

def handleGetRequests(url, headers):
    req = ''
    if headers:
        req = requests.get(url, headers=headers)
    else:
        req = requests.get(url)
    resp = req.json()
    return resp

def getPaginatedData(url, headers, next_key, data_key, key_list):
    dataList = []
    resp = handleGetRequests(url, headers)
    while True:
        for a in resp[data_key]:
            dataList.append({ke: a[ke] for ke in key_list})
        if resp[next_key]:
            resp = handleGetRequests(resp[next_key], headers)
        else:
            break
    return dataList
        

API_BASE = "" #<--- Write your API base here
locale = 'en-us'
api_endpoint = f"/api/v2/help_center/{locale}/articles"
api_url = API_BASE + api_endpoint
keys = ['id', 'html_url', 'body', 'name', 'locale']

all_articles = getPaginatedData(api_url, {}, 'next_page', 'articles', keys)

url_pattern = r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
all_links = []
all_articles_with_links = []
async def searchArticleLink(article, session):
    article_links = []
    article_body = article['body']
    article_a_tags = BeautifulSoup(article_body, 'html.parser').find_all('a')
    
    for tag in article_a_tags:
        try:
            tag_link = tag['href']
        except KeyError:
            tag_link = 'NO URL'

        if(re.match(url_pattern, tag_link)):
            if(not tag_link.startswith('http://') and not tag_link.startswith('https://') and not tag_link.startswith('mailto')):
                if(not bool(re.match(email_pattern, tag_link))):
                    tag_link = 'http://'+tag_link
            status = ''
            repeated = False
            check_dup_link = list(filter(lambda link: link['URL'] == tag_link, all_links))
            if(check_dup_link):
                status = check_dup_link[0]['Status']
                repeated = True
            else:
                try:
                    async with session.get(url=tag_link, ) as response:
                        status = response.status
                except asyncio.exceptions.TimeoutError:
                    status = "Timeout"
                except Exception as e:
                    status = str(e)
                all_links.append({'URL': tag_link, 'Status': status})
            article_links.append({'URL': tag_link, 'Status': status, 'Repeated': repeated})
        else:
            article_links.append({'URL': tag_link, 'Status': 'Not a URL', 'Repeated': False})
                
    article['links'] = article_links
    all_articles_with_links.append(article)
    print(json.dumps(article, sort_keys=True, indent=4))

session_timeout = aiohttp.ClientTimeout(total=10)
async def main(article_list):
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        ret = await asyncio.gather(*[searchArticleLink(a, session) for a in article_list])
    print("Done")
start = time.time()

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main(all_articles))
print(json.dumps(all_articles_with_links, sort_keys=True, indent=4))   


df = pd.DataFrame(all_articles_with_links)
df2 = df.explode('links')

df3 = df2.dropna(axis=0, subset='links')
df4 = pd.DataFrame(df3['links'].apply(lambda x: x['URL']))
df5 = pd.DataFrame(df3['links'].apply(lambda x: x['Status']))
df6 = pd.DataFrame(df3['links'].apply(lambda x: x['Repeated']))

df3.loc[:,'links_clean'] = df4
df3.loc[:,'Status'] = df5
df3.loc[:,'Repeated'] = df6


df3 = df3.drop('links', axis=1)
df3 = df3.drop('body', axis=1)
df3.to_csv("results.csv")

end = time.time()

print("Took {} seconds to pull the data".format(end - start))