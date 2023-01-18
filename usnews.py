import re
import socket
import time
import urllib3

import requests
from bs4 import BeautifulSoup
# from selenium import (webdriver, common)
# from selenium.webdriver.chrome.service import Service


def the_driver():
    # Constants
    web_links = {"item_link": "https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390",
                 "usnews_url": "https://www.usnews.com/"}

    # driver_path_local = r"C:\Users\suman\Documents\Sum\Masters Program\Masters at UCD\Program Related\Syllabus\Q3 " \
    #                     r"Winter\Bax 422 -  Data Design\Class 2\webscraping fun\chromedriver_win32\chromedriver.exe "

    headers = {
        'User-Agent': 'Mozilla/5.0',
    }

    # Function to create a Soup
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

        time.sleep(10)
        soup = BeautifulSoup(r.text, 'lxml')

        return soup

    soup_price = create_soup(web_url=web_links["item_link"], header=headers)

    the_price = soup_price.select(
        "#ProductReview > div.col-sm-12.col-lg-5.pdp-specs-info > div > div.pdp-price > p:nth-child(3) > span.sale-price")[
        0].text

    the_price = re.sub(r",", r"", the_price)
    the_price = re.sub(r"(?s)\$([\d.]+).+", r"\g<1>", the_price)

    list_price = soup_price.select(
        "#ProductReview > div.col-sm-12.col-lg-5.pdp-specs-info > div > div.pdp-price > p.list-price > span:nth-child(3) "
        "> del")[
        0].text

    list_price = re.sub(r",", r"", list_price)
    list_price = re.sub(r"\$([\d.]+)", r"\g<1>", list_price)

    print(f"List Price is {list_price} and the discounted price is {the_price}")

    # news

    soup_news = create_soup(web_url=web_links["usnews_url"], header=headers)

    selector_top_stories = "#app > div.HomePage__PageWrapper-sc-164e2pm-0.hynTJd > div > div:nth-child(1) > div > " \
                           "div.Box-w0dun1-0.ArmRest__Container-z77ov1-0.hTnNtV.bZwypa.Cell-sc-1abjmm4-0-w.iRArip.Cell-sc" \
                           "-1abjmm4-0-w.iRArip > div > div "

    news_text = soup_news.select(selector_top_stories)

    titles_of_stories = news_text[0].findAll("h3")

    titles_of_stories_bellow = news_text[0].findAll("p")

    print("The top stories are: --> ")

    for _ in titles_of_stories:
        print(_.text)

    for _ in titles_of_stories_bellow:
        print(_.text)

    link_second_story = news_text[0].findAll("h3")[1].find("a").get("href")

    print(f"The link of second news story: {link_second_story}")

    soup_news_second_top = create_soup(link_second_story, header=headers)

    selector_para = "#ad-in-text-target"

    the_text = soup_news_second_top.select(selector_para)[0].text

    the_three_sentences = re.sub(r'([^\.?!]+[\.?!])([^\.?!]+[\.?!])([^\.?!]+[\.?!]).+', r"\g<1> \g<2> \g<3>", the_text)

    print(the_three_sentences)


if __name__ == '__main__':
    the_driver()
