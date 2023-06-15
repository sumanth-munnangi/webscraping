import time
import requests
from bs4 import BeautifulSoup
import re


def driver_function():
    # Constants

    diver_path = r"C:\Users\suman\Documents\Sumanth\Masters Program\Masters at UCD\Program Related\Syllabus\Q3 Winter\Bax " \
                 r"422 -  Data Design\Class 2\webscraping fun\chromedriver_win32\chromedriver.exe "

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    creds = {"user_name": "scrapeyouforfree",
             "password": "dontmindme"}

    urls = {"flight_profile": "https://www.planespotters.net/member/profile",
            "flight_login": "https://www.planespotters.net/user/login",
            "flight_base": "https://www.planespotters.net/"}

    session = requests.session()

    r_get_flight = session.get(url=urls['flight_login'], headers=headers)

    time.sleep(10)

    base_cookies = session.cookies.get_dict()

    login_soup = BeautifulSoup(r_get_flight.content, "html.parser")

    def find_hidden_tokens(any_soup):
        """

        :param any_soup: Soup input
        :return: returns the hidden tokens csrf and rid
        """
        try:
            csfr = any_soup.find("input", attrs={"id": "csrf"}).attrs['value']
        except:
            csfr = ""

        try:
            rid = any_soup.find("input", attrs={"id": "rid"}).attrs['value']
        except:
            rid = ""

        return csfr, rid

    print("Base cookies are :")
    print(base_cookies)

    tokens = find_hidden_tokens(login_soup)

    print("The tokens are csrf and rid: ", tokens)

    r_login_flight = session.post(url=urls['flight_login'],
                                  data={"username": creds['user_name'],
                                        "password": creds['password'],
                                        "csrf": tokens[0]},
                                  cookies=base_cookies,
                                  headers=headers)
    time.sleep(10)

    login_cookies = session.cookies.get_dict()

    base_cookies.update(login_cookies)

    out = session.get(url=urls['flight_profile'], cookies=login_cookies, headers=headers)
    time.sleep(10)
    final_soup = BeautifulSoup(out.content, "html.parser")
    print("Login cookies are :")
    print(login_cookies)
    print(final_soup)

    print("Check for user_name, output True if exists: ")

    if re.search(creds['user_name'], final_soup.text):
        print(True)
    else:
        print(False)


if __name__ == '__main__':
    driver_function()
