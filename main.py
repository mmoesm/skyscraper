from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI(title='SkyScraper')

def get_fields(url, params):
    
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html5lib') # TODO: OBS
    
    # Keep the original <br> tags as is:
    for br in soup('br'):
        br.replace_with('\n')

    fields = {'url': url}

    fields['date'] = soup.select_one('.link_green').get_text()
    
    fields['title'] = soup.select_one('p.widetitle').get_text()

    # Tags of interest are partially from dedicated elements and partially embedded in img icon text:
    fields['tags'] = [tag.get_text() for tag in soup.select('span.event_tag')]
    
    fields['icons'] = [tag['title'] for tag in soup.select('div.hidden-xs-down img')]
    
    fields['feed'] = soup.select_one('.condensed > i').get_text()
    fields['feed'] = fields['feed']
    
    # .newsbody encapsulates all paragraphs.
    fields['paragraphs'] = [p.get_text() for p in soup.select('.newsbody > p')]

    fields['tables'] = []
    for table in soup.select('.newsbody table'): 
        fields['tables'].append([[td.text for td in tr.findAll('td')] for tr in table.findAll('tr')])

    return fields

def scrape(url, longitude, latitude, timezone):
    
    params =  {
        'year': 2021,
        'month': 11,
        'longitude': longitude,
        'latitude': latitude,
        'timezone': timezone,
        'maxdiff': 7 # Difficulty (7 is unobservable, so all events are retrieved here.)
    }
    event = get_fields(url, params)
    event['geolocation_id'] = 1337
    return event


@app.get("/")
async def crawl(url: str, longitude: float=10, latitude: float=57, timezone: str='+00:00' ):
    """- Kun nødvendigt at give en event URL, altså fx til [her](https://in-the-sky.org/news.php?id=20211103_19_100). \n
       - Resten kan man indstille valgfrit, hvis man har ondt i numsen over defaults. \n
       - `timezone` er vist med offset i GMT/UTC(?)"""
    return scrape(url, longitude, latitude, timezone)