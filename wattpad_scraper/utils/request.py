# import cloudscraper


# requests = cloudscraper.create_scraper(
#     browser={
#         'browser': 'firefox',
#         'platform': 'windows',
#         'mobile': False
#     }
# )
# response_memory = {}


# def get(url):
#     if url not in response_memory:
#         response_memory[url] = requests.get(url)
#     return response_memory[url]

import httpx
from fake_headers import Headers
import atexit
import os
import pickle
import json

class Cookie:
    """Parse Cookie File For Request"""
    def __init__(self, file):
        super(Cookie, self).__init__()
        self.file = file
        self.keys_to_keep  = ['name', 'value', 'domain', 'path']

    
    def get_cookies_values(self):
        with open(self.file, 'r') as file:
            cookie_data = json.load(file)       
            list_of_cookie_dicts = [{ key: item[key] for key in self.keys_to_keep } for item in cookie_data]
        return list_of_cookie_dicts

    def jar_cookies(self):
        cookies = httpx.Cookies()
        for cookie in self.get_cookies_values():
            cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])
        return cookies.jar



headers = Headers(
    browser='chrome',
    os='Windows',
    headers=True
)
temp_dir_path = "temp_catch_delete_if_not_needed"
if not os.path.exists(temp_dir_path):
    os.mkdir(temp_dir_path)

res_path = os.path.join(temp_dir_path, "response_memory.pickle")
session_path = os.path.join(temp_dir_path, "session.pickle")


def store_response():
    # store response memory in pickle file
    with open(os.path.join(temp_dir_path, "response_memory.pickle"), "wb") as f:
        pickle.dump(response_memory, f)

def load_response():
    # load response memory from pickle file
    if os.path.exists(res_path):
        with open(res_path, "rb") as f:
            response_memory = pickle.load(f)
    else:
        response_memory = {}
    return response_memory

def login(username,password):
    login_endpoint  ="https://www.wattpad.com/login?nextUrl=%2Fhome"
    data = {
        "username": username,
        "password": password
    }
    session.post(login_endpoint,data=data,headers=headers)


def cookie_login(file):
    cookie = Cookie(file)
    cookie_jar = cookie.jar_cookies()
    login_endpoint = "https://www.wattpad.com/login"
    session.cookies.jar = cookie_jar
    session.follow_redirects = True
    response = session.post(login_endpoint,headers=headers)
    data = get_user_details(response.text)
    os.environ['WATTPAD_USERNAME'] = data['username']

os.environ['USER_LOGGED_IN'] = ''

headers = headers.generate()
response_memory = load_response()


session = httpx.Client(headers=headers)

def user_login():
    if not os.environ['USER_LOGGED_IN']:
        if "WATTPAD_USERNAME" in os.environ and "WATTPAD_PASSWORD" in os.environ:
            login(os.environ['WATTPAD_USERNAME'],os.environ['WATTPAD_PASSWORD'])
        elif "WATTPAD_COOKIE_FILE" in os.environ:
            cookie_login(os.environ['WATTPAD_COOKIE_FILE'])
        os.environ['USER_LOGGED_IN'] = 'True'

def get(url):
    user_login()

    if url not in response_memory:
        response_memory[url] = session.get(url)
    return response_memory[url]

def close():
    session.close()
    store_response()

atexit.register(close)