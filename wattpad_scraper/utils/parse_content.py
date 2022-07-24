from typing import List
from .request import get
from bs4 import BeautifulSoup

def chapter_soups(url : str, page: int=1, prev_soups:List[BeautifulSoup]=[]) -> BeautifulSoup:
    res = get(url + '/page/' + str(page))
    soup = BeautifulSoup(res.text, "html.parser")
    prev_soups.append(soup)

    # check if more content is available class on-load-more-page
    more_content = soup.find(class_='on-load-more-page')
    # print('page: ' + str(page), more_content != None)
    if more_content is not None:
        return chapter_soups(url, page+1, prev_soups)
    else:
        return prev_soups

def parse_content(url : str) -> List[str]:
    """parse wattpad chapters

    Args:
        url (string): chapter url

    Returns:
        list: returns a list of content ether a text or a img url
    """
    soups = chapter_soups(url)
    # print('len(soups): ' + str(len(soups)))
    contents = []

    for soup in soups:
        ptags = soup.select('p[data-p-id]')
        for p in ptags:
            # check if if p tag have img tag
            if p.find('img') is not None:
                # if p tag have img tag, get img tag src
                img_url = p.find('img').get('src')
                if img_url.startswith('/'):
                    img_url = 'https://www.wattpad.com' + img_url
                contents.append(img_url)
            else:
                # if p tag don't have img tag, get text
                contents.append(p.get_text())
    return contents
