from bs4 import BeautifulSoup
import requests


def custom_hn(links, subtext):
    hn = []
    for ids, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[ids].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ' '))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return  sorted_by_stories(hn)


def sorted_by_stories(hnlist):
    return sorted(hnlist, key=lambda key: key['votes'], reverse=True)


res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.storylink')
links2 = soup2.select('.storylink')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

all_links = links + links2
all_subtexts = subtext + subtext2

for item in custom_hn(all_links, all_subtexts):
    print(item)
