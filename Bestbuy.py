import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def driver_function():
    diver_path = r"C:\Users\suman\Documents\Sumanth\Masters Program\Masters at UCD\Program Related\Syllabus\Q3 Winter\Bax " \
                 r"422 -  Data Design\Class 2\webscraping fun\chromedriver_win32\chromedriver.exe "

    link = "https://bestbuy.com/"

    try:
        os.makedirs(os.getcwd() + "\\sumanth_html_files")
    except:
        pass

    print("Created a folder to store html files")

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

    s = Service(diver_path)

    driver = webdriver.Chrome(service=s)

    driver.get(link)

    print("Established the connection")

    driver.find_element(By.LINK_TEXT, "Deal of the Day").click()
    time.sleep(5)
    print("Clicked on Deal of the Day")
    the_time_left = driver.find_element(By.CLASS_NAME, "countdown-clock").text
    print("Getting the time left")

    the_time_left = the_time_left.replace("\n", " ").replace(":", "and")

    print(the_time_left)

    time.sleep(8)

    driver.find_element(By.CLASS_NAME, "wf-offer-link").click()
    print("Clicked on the deal (The actual deal)")
    time.sleep(5)

    driver.find_element(By.CLASS_NAME, "ugc-c-review-average").click()
    time.sleep(6)
    print("Clicked on reviews")
    deal_soup = BeautifulSoup(driver.page_source, "html.parser")

    path_html = os.getcwd()

    path_html = path_html + "\\sumanth_html_files"
    print("writing html file")
    write_html(path_html + "\\bestbuy.html", deal_soup)
    driver.close()


if __name__ == '__main__':
    driver_function()
