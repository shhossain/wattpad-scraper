
import httpx
from fake_headers import Headers
import atexit
import os
import json
import re
from bs4 import BeautifulSoup
from .request import user_login

headers = Headers(
    browser='chrome',
    os='Windows',
    headers=True
)

def access_for_authentcated_user(func):
    def is_authenticated(*args, **kwargs):
        if not os.environ['USER_LOGGED_IN']:
            return "No Access Until Logged In"
        else:
            func(*args, **kwargs)
    return is_authenticated

def error(str):
    raise ValueError(str)

@access_for_authentcated_user
def get_user_details(data=None):
    if data == None:
        response = session.post('https://www.wattpad.com/home')
        data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    scripts = soup.find_all('script')
    script = [script for script in scripts if "wattpad.user =" in script.text][0].text
    pattern = re.compile(r"wattpad.user = (.*?);$", re.MULTILINE | re.DOTALL)
    scriptParse = re.search(pattern, str(script))
    userData = json.loads(scriptParse.groups(1)[0])
    return userData



class ReadingList:
    """Actions that can be performed on users ReadingList"""
    def __init__(self):
        user_login()

    @access_for_authentcated_user
    def create_reading_list(self, Title):
        json_data = {
        'id': None,
        'name': Title,
        'numStories': 0,
        'cover': 0,
        'tags': [],
        'featured': False,
        'action': 'create',
        }
        response = session.post('https://www.wattpad.com/api/v3/lists/', headers=headers, json=json_data)
        if response.status_code == 200:
            print(f'{Title} - Reading List was Successfully Created !!!')
            return True
        else:
            print(response.json()['message'])
            return False

    def author_book_list(self, author_username):
        response = session.get(f"https://www.wattpad.com/v4/users/{author_username}/stories/published?offset=0&limit=102")
        return response.json()

    def get_reading_list(self, id=None, title=None, username=None):
        if username == None:
            username = error("No Access Until Logged In") if not os.environ['USER_LOGGED_IN'] else os.environ['WATTPAD_USERNAME']
        response = session.get(f"https://www.wattpad.com/api/v3/users/{username}/lists")
        reading_list = response.json()['lists']
        if title != None or id != None:
            if title != None:
                reading_list = [ a for a in reading_list if a['name'] == title ]
            elif id != None:
                reading_list = [ a for a in reading_list if a['id'] == id ]
            return reading_list[0] if len(reading_list) > 0 else error("Reading List Does Not Exist !!")
        return reading_list

    @access_for_authentcated_user
    def delete_reading_list(self, Title):
        id = get_reading_list(title=Title)['id']
        response = session.delete(f'https://www.wattpad.com/api/v3/lists/{id}', headers=headers)
        # print(response, response.text,id, type(id))
        if response.status_code == 200:
            print(f'{Title} - Reading List was Successfully Deleted !!!')
            return True
        else:
            print(response.json()['message'])
            return False

    @access_for_authentcated_user
    def add_to_reading_list(self, idOfBook=None, urlOfBook=None, titleOfReadingList=None, idOfReadingList=None):
        book_id = idOfBook if urlOfBook == None else (urlOfBook.split("/"))[-1].split("-")[0]
        data = {
        'stories': str(book_id),
        }
        reading_list = idOfReadingList if titleOfReadingList == None else get_reading_list(title=titleOfReadingList)['id']
        response = session.post(f'https://www.wattpad.com/api/v3/lists/{str(reading_list)}/stories', headers=headers, data=data)
        if response.status_code == 200:
            print(f'The Book was Successfully Addeed to {get_reading_list(id=reading_list)["name"]}!!!')
            return True
        else:
            print(response.json()['message'])
            return False


headers = headers.generate()



session = httpx.Client(headers=headers)




def close():
    session.close()

atexit.register(close)