import os
import re
import time
import requests
import socket
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pymongo
import json

diver_path = r"C:\Users\suman\Documents\Sumanth\Masters Program\Masters at UCD\Program Related\Syllabus\Q3 Winter\Bax " \
             r"422 -  Data Design\Class 2\webscraping fun\chromedriver_win32\chromedriver.exe "

cp = os.getcwd()


# headers = {'User-Agent': 'Mozilla/5.0'}


# Utility Functions

def create_soup(web_url):
    """
    :param web_url: URL for the website
    :param header: User Agent :)
    :return: Returns the BeautifulSoup object
    """

    try:
        r = requests.get(url=web_url, timeout=5, stream=True)

    except (socket.timeout, requests.exceptions.ReadTimeout, urllib3.exceptions.ReadTimeoutError) as error:
        return print(error)

    time.sleep(5)
    soup = BeautifulSoup(r.text, 'lxml')

    return soup


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


def q1_selenium():
    print("\n\nSelenium:  The Bored Ape Yacht Club\n\n\n")

    apes_link = "https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][" \
                "name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold "

    s = Service(diver_path)

    driver = webdriver.Chrome(service=s)

    time.sleep(2)
    driver.get(apes_link)

    time.sleep(2)

    for _ in range(1, 9):
        xpath_ape = f"//*[@id='main']/div/div/div/div[5]/div/div[7]/div[3]/div[2]/div/div[{_}]"

        # find_loc = driver.find_element(By.XPATH, xpath_ape).location
        the_ape = driver.find_element(By.XPATH, xpath_ape)
        find_cor = the_ape.size
        action = ActionChains(driver)
        driver.execute_script("arguments[0].scrollIntoView();", the_ape)
        time.sleep(2)
        action.move_to_element_with_offset(to_element=the_ape,
                                           xoffset=find_cor['width'] / 5,
                                           yoffset=find_cor['height'] / 5).click().perform()
        time.sleep(10)
        print(f"clicked on the {_} th/nd costly ape with Solid gold fur")
        ape_soup = BeautifulSoup(driver.page_source, "html.parser")
        path_ape_htm = cp + f"\\bayc_{_}.htm"
        write_html(path_ape_htm, soup=ape_soup)
        time.sleep(5)
        driver.back()
        time.sleep(8)

    driver.close()


def q3_mongo():
    print("\n\n MongoDB Q 3\n\n\n")

    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mongo_client["ddr_project_2"]
    collect = mydb["bayc"]

    # collect.insert()

    all_collections = []

    for _ in range(1, 9):
        file_path = os.getcwd() + f"\\bayc_{_}.htm"

        ape_soup = open_html(file_path)

        ape_name = ape_soup.find("h1", attrs={"class": "sc-29427738-0 hKCSVX item--title"}).text.strip()

        ape_collection = {"name": ape_name}

        attributes = ape_soup.findAll("div", attrs={"class": "sc-d6dd8af3-0 hkmmpQ item--property"})

        for _ in range(len(attributes)):
            att_name = attributes[_].find("div", attrs={"class": "Property--type"}).text.strip()

            att_value = attributes[_].find("div", attrs={"class": "Property--value"}).text.strip()

            att_rarity = attributes[_].find("div", attrs={"class": "Property--rarity"}).text.strip()

            ape_collection[att_name] = {"value": att_value, "rarity": att_rarity}

        all_collections.append(ape_collection)

    collect.insert_many(all_collections)

    for _ in collect.find({}):
        print("\n\n")
        print(_)


# Regular Webscraping

def q5_regular_web():
    yp_url = "https://www.yellowpages.com/search?search_terms=Pizzeria&geo_location_terms=San%Francisco"
    yp_base_url = "https://www.yellowpages.com"

    yp_full_soup = create_soup(yp_url)
    yp_full_write_path = os.getcwd() + "\\sf_pizzeria_search_page.htm"

    write_html(soup=yp_full_soup, path=yp_full_write_path)

    yp_read_soup = open_html(yp_full_write_path)

    yp_top_30 = yp_read_soup.findAll("div", attrs={"class": "result"})

    all_shops = []

    for _ in range(len(yp_top_30)):

        shop_info = {}

        s_title = yp_top_30[_].find("h2", attrs={"class": "n"}).text

        s_title = s_title.replace("\n", "")

        s_rank = s_title.split(".")[0].replace(" ", "")

        s_name = s_title.split(".")[1].strip()

        linked_url = yp_top_30[_].find("h2", attrs={"class": "n"}).find("a").get("href")
        linked_url = yp_base_url + linked_url
        shop_info.update({"search_rank": s_rank, "name": s_name, "linked_URL": linked_url})

        try:
            yp_tripadvisor = yp_top_30[_].find("div", attrs={"class": "ratings"}).get("data-tripadvisor")
            yp_tripadvisor = json.loads(yp_tripadvisor)
            shop_info.update({"TripAdvisor_rating": yp_tripadvisor['rating'],
                              "Number_tripadvisor": yp_tripadvisor['count']})
        except Exception as e:
            print("No tripadvisor ratings")

        rating_match = {"one": 1,
                        "two": 2,
                        "three": 3,
                        "four": 4,
                        "five": 5}

        try:
            star_rating = yp_top_30[_].find("div", attrs={"class": "result-rating"}).get("class")[1]
            star_rating_count = yp_top_30[_].find("span", attrs={"class": "count"}).text.replace(" ", "").replace("\n",
                                                                                                                  "") \
                .replace("(", "").replace(")", "")
            shop_info.update({"star_ratings": rating_match[star_rating],
                              "star_rating_count": star_rating_count})
        except Exception as e:
            print("No star rating")

        try:
            yp_price_range = yp_top_30[_].find("div", attrs={"class": "price-range"}).text.strip()
            shop_info.update({"price_range": yp_price_range})
        except Exception as e:
            print("No Price Range")

        try:
            yp_year_bus = yp_top_30[_].find("div", attrs={"class": "number"}).text.strip()
            shop_info.update({"Years_in_business": yp_year_bus})
        except Exception as e:
            print("No Number of years in Business")

        try:
            yp_reviews = yp_top_30[_].find("p", attrs={"class": "body with-avatar"}).text.strip()
            shop_info.update({"reviews": yp_reviews})
        except Exception as e:
            print("No Reviews")

        try:
            yp_amenities = yp_top_30[_].find("div", attrs={"class": "amenities-info"}).findAll("span")
            yp_amenities = [x.text.strip() for x in yp_amenities]
            shop_info.update({"amenities": yp_amenities})
        except Exception as e:
            print("No Reviews")

        all_shops.append(shop_info)

    for _ in all_shops:
        print(_)


def q6_mongodb():
    print("\n\n\n Q Mongo DB \n\n\n")

    yp_base_url = "https://www.yellowpages.com"

    yp_full_write_path = os.getcwd() + "\\sf_pizzeria_search_page.htm"

    yp_read_soup = open_html(yp_full_write_path)

    yp_top_30 = yp_read_soup.findAll("div", attrs={"class": "result"})

    all_shops = []

    for _ in range(len(yp_top_30)):

        shop_info = {}

        s_title = yp_top_30[_].find("h2", attrs={"class": "n"}).text

        s_title = s_title.replace("\n", "")

        s_rank = s_title.split(".")[0].replace(" ", "")

        s_name = s_title.split(".")[1].strip()

        linked_url = yp_top_30[_].find("h2", attrs={"class": "n"}).find("a").get("href")
        linked_url = yp_base_url + linked_url
        shop_info.update({"search_rank": s_rank, "name": s_name, "linked_URL": linked_url})

        try:
            yp_tripadvisor = yp_top_30[_].find("div", attrs={"class": "ratings"}).get("data-tripadvisor")
            yp_tripadvisor = json.loads(yp_tripadvisor)
            shop_info.update({"TripAdvisor_rating": yp_tripadvisor['rating'],
                              "Number_tripadvisor": yp_tripadvisor['count']})
        except Exception as e:
            print("No tripadvisor ratings")

        rating_match = {"one": 1,
                        "two": 2,
                        "three": 3,
                        "four": 4,
                        "five": 5}

        try:
            star_rating = yp_top_30[_].find("div", attrs={"class": "result-rating"}).get("class")[1]
            star_rating_count = yp_top_30[_].find("span", attrs={"class": "count"}).text.replace(" ", "").replace("\n",
                                                                                                                  "") \
                .replace("(", "").replace(")", "")
            shop_info.update({"star_ratings": rating_match[star_rating],
                              "star_rating_count": star_rating_count})
        except Exception as e:
            print("No star rating")

        try:
            yp_price_range = yp_top_30[_].find("div", attrs={"class": "price-range"}).text.strip()
            shop_info.update({"price_range": yp_price_range})
        except Exception as e:
            print("No Price Range")

        try:
            yp_year_bus = yp_top_30[_].find("div", attrs={"class": "number"}).text.strip()
            shop_info.update({"Years_in_business": yp_year_bus})
        except Exception as e:
            print("No Number of years in Business")

        try:
            yp_reviews = yp_top_30[_].find("p", attrs={"class": "body with-avatar"}).text.strip()
            shop_info.update({"reviews": yp_reviews})
        except Exception as e:
            print("No Reviews")

        try:
            yp_amenities = yp_top_30[_].find("div", attrs={"class": "amenities-info"}).findAll("span")
            yp_amenities = [x.text.strip() for x in yp_amenities]
            shop_info.update({"amenities": yp_amenities})
        except Exception as e:
            print("No Reviews")

        all_shops.append(shop_info)

    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mongo_client["ddr_project_2"]
    collect = mydb["sf_pizzerias"]

    collect.insert_many(all_shops)


def q78_parsing():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mongo_client["ddr_project_2"]
    collect = mydb["sf_pizzerias"]

    list_of_links = list(collect.find({}, {"linked_URL": 1}))

    list_of_links = [x['linked_URL'] for x in list_of_links]

    counter = 1
    for _ in list_of_links:

        while True:
            try:
                the_soup = create_soup(_)
                break
            except:
                time.sleep(8)
                continue

        time.sleep(8)
        yp_path_down = cp + f"\\sf_pizzerias_{counter}.htm"
        write_html(yp_path_down, the_soup)
        counter += 1

    all_yp_places = []

    for _ in range(1, 31):
        place_details = {}
        yp_path_down = cp + f"\\sf_pizzerias_{_}.htm"

        soup_yp = open_html(yp_path_down)

        the_section = soup_yp.find("section", attrs={"class": "inner-section"})
        try:
            phone_number = the_section.find("a", attrs={"class": "phone dockable"}).text.strip()
            place_details['phone_number'] = phone_number
        except:
            print("no Phone number")
        try:
            address = the_section.find("span", attrs={"class": "address"}).text.strip()
            address = re.sub("[ +]{2}", '', address)
            address = re.sub("\n", ' ', address)
            address = re.sub("[ +]{2}", ', ', address)
            place_details['address'] = address
        except:
            print("No address")

        try:
            web_link = the_section.find("a", attrs={"class": "website-link"}).get("href")
            place_details['web_link'] = web_link
        except:
            print("No website")

        all_yp_places.append(place_details)

    for _ in all_yp_places:
        print(_)
        print("\n\n")
    return all_yp_places


def q9_api(all_yp_places):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mongo_client["ddr_project_2"]
    collect = mydb["sf_pizzerias"]
    api_key = "408ddf0ab2c8975442b4cdc44cf4c427"
    counter = 0

    for _ in all_yp_places:
        address = _['address']
        params = {
            'access_key': api_key,
            'query': address,
            'limit': 1,
        }

        while True:
            try:
                conn = requests.get(url='http://api.positionstack.com/v1/forward?', params=params)
                time.sleep(8)

                the_json = conn.json()['data'][0]

                needed = {i: j for i, j in the_json.items() if i in ['latitude', 'longitude']}
                temp = all_yp_places[counter]
                temp.update(needed)
                all_yp_places[counter] = temp

                break
            except:
                print("Retry", address)
                continue

        counter += 1

    for docu, newvalues in zip(collect.find(), all_yp_places):
        update = {"$set": newvalues}
        collect.update_one({"search_rank": docu["search_rank"]}, update)


if __name__ == "__main__":
    q1_selenium()
    q3_mongo()
    q5_regular_web()
    q6_mongodb()
    all_yp_places = q78_parsing()
    q9_api(all_yp_places)
