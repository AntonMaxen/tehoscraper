import os
from dotenv import load_dotenv

import requests
from writefile import is_new_source, reset_sources
from bs4 import BeautifulSoup


load_dotenv()
USERNAME = os.getenv('PP_USERNAME')
PASSWORD = os.getenv('PP_PASSWORD')


LOGIN_URL = "https://yh.pingpong.se/login/processlogin?disco=local"
URL = "https://yh.pingpong.se/courseId/11264/content.do?id=4744630"
BASE_URL = "https://yh.pingpong.se"
FILENAME = "sources.txt"

# Set this to true to test behaviour of empty file
want_reset = False


def upload_new_source():
    pass


def main():
    if want_reset:
        reset_sources(FILENAME)

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

    for source in sources:
        if is_new_source(source, FILENAME):
            print(f'Uploading: {source} to discord')
    pass


if __name__ == '__main__':
    main()
