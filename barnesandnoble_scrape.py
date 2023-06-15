import socket
import time
import urllib3
import os
import requests
from bs4 import BeautifulSoup

item_count = 40
page = 1
web_links = {
    "page_link": "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp={}&page={}".format(item_count, page)}

headers = {
    'User-Agent': 'Mozilla/5.0',
}

base_url = "https://www.barnesandnoble.com/"


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

    time.sleep(5)
    soup = BeautifulSoup(r.text, 'lxml')

    return soup


# Use the URL identified above and write code that loads the first page with 40 items per page of “B&N Top 100”.
print("Question 1")
soup_book = create_soup(web_url=web_links["page_link"], header=headers)
print(f"Created the soup for {web_links['page_link']}")


def get_the_final_link(from_soup, url=base_url):
    """
    :param url: The base URL
    :param from_soup: The soup tag
    :return: the final link
    """
    final_url = url + from_soup.find("a").get("href")

    return final_url


# Take your code in (a) and create a list of each book’s product page URL. This list should be of length 40.
print("Question 2")
thesoup = soup_book.findAll("h3", attrs={"class": "product-info-title"})

links = [get_the_final_link(x) for x in thesoup]

print(f"There are {len(links)} links in this page")

# write page source content to file

print("Downloading all the html files. this will take some time.")
os.mkdir("data_sumanth")
# writing html files
for _ in range(0, 40):
    soup_book = create_soup(web_url=links[_], header=headers)
    time.sleep(5)
    try:
        name = soup_book.title.text
    except:
        name = "No Title"

    path = os.getcwd() + "\\data_sumanth\\" + str(_) + ".html"

    with open(path, 'w', encoding="utf-8") as file:
        file.write(soup_book.prettify())
    time.sleep(1)
    file.close()
    print(f"Done with {name}")
    if _ == 39:
        print("Done will all :)")

# reading the html files
for _ in range(0, 40):
    path = os.getcwd() + "\\data_sumanth\\" + str(_) + ".html"
    with open(path, 'r', encoding="utf-8") as file:
        html_content = file.read()
        soup_book = BeautifulSoup(html_content, 'html.parser')
        print(soup_book.findAll("div", {"class": "bs-content"})[0].text[:100])
        try:
            name = soup_book.title.text
        except:
            name = "No Title"
        print(f"Done with {name}")
        time.sleep(0.5)
    if _ == 39:
        print("Done will all :)")
