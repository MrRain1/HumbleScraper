import json
from os import mkdir
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

PAGES = ["games", "books", "software"]


def writeData(data_to_write, type):
    """Dumps the dictionary in a JSON file

    Args:
        data_to_write (dictionary): dict containing all the bundles in a category
        type (string): bundle category name
    """
    try:
        with open(f"data/{type}.json", "w") as doc_to_write:
            json.dump(data_to_write, doc_to_write, indent=4)
    except FileNotFoundError:
        print("Directory not found! Creating a new one...")
        mkdir("data")
        with open(f"data/{type}.json", "w") as doc_to_write:
            json.dump(data_to_write, doc_to_write, indent=4)


def webDriver(path):
    """Navigate to the HB page and return the HTML page

    Args:
        path (string): Path to the bundle webpage

    Returns:
        string: HTML webpage
    """
    driver.get(f"https://www.humblebundle.com/{path}")
    return driver.page_source


def scrapeBundles(elems):
    count = 1
    data = {}
    for item in elems:
        bundle_name = item.find("span", class_="name").text.strip()

        try:
            bundle_time_left = item.find(
                "div", class_="js-countdown-timer timer-wrapper button-v2 oval-button red")['aria-label']
        except:
            bundle_time_left = item.find(
                "div", class_="js-countdown-timer timer-wrapper button-v2 oval-button red is-hidden")['aria-label']

        new_data = {
            "name": bundle_name,
            "time left": bundle_time_left
        }

        data[count] = new_data
        count += 1
    return data


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(service=FirefoxService(
    GeckoDriverManager().install()), options=options)

data = {}

try:
    soup_games = BeautifulSoup(webDriver("games"), "html.parser")
    soup_books = BeautifulSoup(webDriver("books"), "html.parser")
    soup_software = BeautifulSoup(webDriver("software"), "html.parser")
except TypeError:
    raise TypeError("None Type")
finally:
    driver.quit()

bundles = [soup_games.find_all("div", class_="info-section"),
           soup_books.find_all("div", class_="info-section"),
           soup_software.find_all("div", class_="info-section")]

for index in range(len(bundles)):
    dict_to_append = scrapeBundles(bundles[index])
    data[PAGES[index]] = dict_to_append
    writeData(data, PAGES[index])
    data.clear()

print("Done!")