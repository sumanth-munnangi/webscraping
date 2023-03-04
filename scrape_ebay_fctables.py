import re
import os
import socket
import time
import urllib3
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

page = 1

web_urls = {"ebay_page": f"https://www.ebay.com/sch/i.html?_nkw=amazon+gift+card&_sacat=0&LH_Sold=1&_pgn={page}"}

creds = {"userid": "scrapemeforfree", "pass": "shurewhynot"}

data_creds = {"login_username": creds["userid"],
              "login_password": creds["pass"],
              "login_action": 1,
              "user_remeber": 1
              }

web_url_session = "https://www.fctables.com/user/login/"
bets_url = "https://www.fctables.com/tipster/my_bets/"

headers = {
    'User-Agent': 'Mozilla/5.0',
}


def create_soup(web_url, header):
    """
    :param web_url: URL for the website
    :param header: User Agent :)
    :return: Returns the BeautifulSoup object
    """

    try:
        r = requests.get(url=web_url, timeout=5, headers=header, stream=True)

    except (socket.timeout, requests.exceptions.ReadTimeout, urllib3.exceptions.ReadTimeoutError) as error:
        return print(error)

    time.sleep(5)
    soup = BeautifulSoup(r.text, 'lxml')

    return soup


os.mkdir("html_files_sumanth")

path_amz_01 = os.getcwd() + "\\html_files_sumanth\\" + "amazon_gift_card_01.html"

soup_first_page = create_soup(web_urls["ebay_page"], headers)

print("Downloading the html file for sold amazon gift card")


def write_html(path, soup):
    """
    :param path: path where the html file needs to be downloaded
    :param soup: soup
    :return: downloads the file in the folder
    """
    with open(path, 'w', encoding="utf-8") as file:
        file.write(soup.prettify())
    time.sleep(2)
    file.close()
    print(f"Done downloading file at {path}")


def open_html(path):
    """
    :param path: path of the html file
    :return: return soup
    """
    with open(path, 'r', encoding="utf-8") as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        print(f"Opening the file at {path}")
    return soup


def get_details(items):
    """
    :ivar items: item tags
    :return: a list of dictionary with key information
    """
    list_items = []

    for _ in items:
        price_details = _.find("span", attrs={"class": "s-item__price"}).text.strip().replace("\n", "")
        try:
            shipping_details = _.find("span",
                                      attrs={"class": "s-item__shipping s-item__logisticsCost"}).text.strip().replace(
                "\n", "")
        except:
            print("no shipping details")
            shipping_details = "$0"
        title = _.find("div", attrs={"class": "s-item__title"}).text.strip().replace("\n", "").replace("  ", "")
        try:
            price = float(re.sub("\$", "", price_details))
        except:
            print("Price range; Taking max possible price")
            price = float(re.sub(".+?([\d.]+).+?([\d.]+)", "\g<2>", price_details))

        try:
            shipping_fee = float(re.sub("[+\$]+([\d.]+).+", "\g<1>", shipping_details))
        except ValueError as e:
            shipping_fee = 0
        total_price = price + shipping_fee
        try:
            value = float(re.sub(".*?(\$)([\d.]+).*", "\g<2>", title))
        except ValueError as e:
            value = 0
        list_items.append({"title": title,
                           "price": price,
                           "shipping_fee": shipping_fee,
                           "total_price": total_price,
                           "value": value})

    return list_items


# Question B

write_html(path_amz_01, soup_first_page)

# Question C

for page in range(2, 11):

    web_url = f"https://www.ebay.com/sch/i.html?_nkw=amazon+gift+card&_sacat=0&LH_Sold=1&_pgn={page}"

    if page < 10:
        path_amz = os.getcwd() + "\\html_files_sumanth\\" + f"amazon_gift_card_0{page}.html"
    else:
        path_amz = os.getcwd() + "\\html_files_sumanth\\" + f"amazon_gift_card_{page}.html"

    print(web_url)
    soup_page = create_soup(web_url, headers)

    write_html(path_amz, soup_page)
    time.sleep(8)

# Create a dummy dataframe

#  Question D and E
item_details_df = pd.DataFrame(columns=["title", "price", "shipping_fee", "total_price", "value"])

for page in range(1, 11):

    if page < 10:
        path_amz = os.getcwd() + "\\html_files_sumanth\\" + f"amazon_gift_card_0{page}.html"
    else:
        path_amz = os.getcwd() + "\\html_files_sumanth\\" + f"amazon_gift_card_{page}.html"

    soup_page = open_html(path_amz)

    all_items = soup_page.find("ul", attrs={"class": "srp-results srp-list clearfix"}) \
        .findAll("div", attrs={"class": "s-item__info clearfix"})

    list_of_details = get_details(all_items)

    print(f"All items from page {page}")
    print(f"There are {len(all_items)} items in this page")

    for _ in list_of_details:
        for i, j in _.items():
            print(f"{i}:{j}")

    item_details_df = pd.concat([item_details_df, pd.DataFrame(list_of_details)], axis=0, ignore_index=True)

# Question F

profit_percentage = np.mean(item_details_df['value'] < item_details_df['total_price']) * 100

item_details_df.head(5)

print(f"{profit_percentage} % of products from first 10 pages are sold for a higher price compared to their value. "
      f"Ebay lets sellers fix their prices depending on the demand. Looks like people are willing to buy gift "
      f"cards for far more than their worth.")

print("-------------------------- Question 2 ------------------------")


session = requests.session()

r_login = session.post(web_url_session,
                       data=data_creds,
                       timeout=5)

cookies = session.cookies.get_dict()

print("Logged into fctables :). Printing the cookies ----------")

print(cookies)

print("getting my_bets")
time.sleep(10)

bets_session = session.get(url=bets_url, cookies=cookies)

bet_soup = BeautifulSoup(bets_session.content, 'html.parser')

output_bet = bet_soup.find("div", attrs={"class": "coupon-items"})

print(output_bet.text)

write_html(os.getcwd() + "\\html_files_sumanth\\" + "fctables_bets.html", bet_soup)
