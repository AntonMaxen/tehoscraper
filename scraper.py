import os
from dotenv import load_dotenv

import requests
from writefile import is_new_source
from bs4 import BeautifulSoup
from config import LOGIN_URL, URL, BASE_URL


load_dotenv()
USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')


# Returns array of sources that's new according to sources txt file.
def find_new_sources(filename):
    session_requests = requests.session()

    payload = {
        "login": USERNAME,
        "password": PASSWORD
    }

    login_result = session_requests.post(LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))
    print(login_result)
    id_result = session_requests.get(URL, headers=dict(referer=URL))
    soup = BeautifulSoup(id_result.content, 'html.parser')
    ppfdata = soup.find(id='ppfdata')['src']
    content_request_url = BASE_URL + ppfdata
    content_result = session_requests.get(content_request_url, headers=dict(referer=content_request_url))
    parsed_content = BeautifulSoup(content_result.content, 'html.parser')
    iframes = parsed_content.find_all('iframe')
    sources = ['https:' + src['src'] for src in iframes]
    new_sources = []

    for source in sources:
        if is_new_source(source, filename):
            new_sources.append(source)
            print(f'Found a new source: {source} adding it to the queue')

    return new_sources


if __name__ == '__main__':
    pass
