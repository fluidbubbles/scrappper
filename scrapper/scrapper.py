import logging
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
import matplotlib.pyplot as plt
from db.session import engine
from utils.utils import remove_blanks, get_event_data, print_progress_bar
import pathlib

base_url = "https://www.lucernefestival.ch"
program_url = "en/program/summer-festival-22"
log = logging.getLogger(__name__)
session = HTMLSession()


def scrape():
    log.info("Crawling started")
    html_text = session.get(f'{base_url}/{program_url}').text
    soup = BeautifulSoup(html_text, 'lxml')
    events = soup.find_all('div', class_='entry')

    rows_list = []
    print_progress_bar(0, len(events[1:-5]), prefix='Progress:', suffix='Complete', length=50)
    for i, event in enumerate(events[1:-5]):
        get_event = session.get(f"{base_url}/{event.find_all('a', class_='detail')[0].attrs.get('href')}")
        get_event_data(get_event)
        event_pg_soup = BeautifulSoup(get_event.html.html, "lxml")

        date = event.get("data-date")
        time = event.find('span', class_='time').text
        location = remove_blanks(event.find('p', class_='location').text)
        title = remove_blanks(event.find('p', class_='surtitle').text)
        image_link = event.find('div', class_='image').attrs.get('style')[16:-16]

        artists = [remove_blanks(artist.contents[1].text)
                   for artist in event_pg_soup.find_all("div", class_="artist")]

        works = [remove_blanks(work.text) for work in event_pg_soup.find_all("div", class_="musical-piece")]

        description_text = remove_blanks(event_pg_soup.find_all("div", class_="description-text")[0].text)
        price_div = event_pg_soup.find_all("div", class_="middle")[0].find_all("p")
        price_comments = None
        currency = None
        ticket_price = None
        if len(price_div) >= 2:
            price_data = price_div[1].text.split()
            currency = price_data[0]
            ticket_price = price_data[1:]

        if len(price_div) == 1 or len(price_div) == 3:
            price_comments = price_div[len(price_div) - 1].text

        data_dict = {'date': date,
                     'time': time,
                     'location': location,
                     'title': title,
                     'artists': artists,
                     'works': works,
                     'ticket_price': ticket_price,
                     'currency': currency,
                     'price_comments': price_comments,
                     'description': description_text,
                     'image_link': image_link
                     }

        rows_list.append(data_dict)
        print_progress_bar(i + 1, len(events[1:-5]), prefix='Progress:', suffix='Complete', length=50)
    log.info("Successfully finished crawling")
    return rows_list


def add_to_db(data):
    log.info("Adding to DB")
    df = pd.DataFrame(data)
    df.to_sql('events', engine, if_exists='replace')
    log.info("Successfully added to DB")


def plot_data():
    log.info("Extracting Data from DB")
    df_result = pd.read_sql('select date, count(date) as events from events group by date order by 1,2', engine)
    log.info("Generating Plot")
    df_result.plot(x="date", y="events", kind="bar", figsize=(15, 10))
    plt.show()
    log.info("Saving Plot")
    plt.savefig(f'{str(pathlib.Path().resolve())}/plot.png')
    log.info(f"Plot saved at{str(pathlib.Path().resolve())}/plot.png")


def run():
    scrapped_data = scrape()
    add_to_db(scrapped_data)
    plot_data()
