import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def driver_function():
    diver_path = r"C:\Users\suman\Documents\Sumanth\Masters Program\Masters at UCD\Program Related\Syllabus\Q3 Winter\Bax " \
                 r"422 -  Data Design\Class 2\webscraping fun\chromedriver_win32\chromedriver.exe "

    link = "https://www.google.com"

    s = Service(diver_path)

    driver = webdriver.Chrome(service=s)

    def google_something(the_driver, search):
        """
        :param the_driver: selenium driver
        :param search: search text
        :return:
        """
        the_driver.get(link)
        time.sleep(5)
        the_driver.find_element("name", "q").send_keys(search + "\n")
        time.sleep(5)
        print(f"Done searching for {search}")

    google_something(driver, "askew")

    google_something(driver, "google in 1998")

    driver.close()


if __name__ == '__main__':
    driver_function()
