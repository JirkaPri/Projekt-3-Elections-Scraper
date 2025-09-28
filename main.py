"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Jiří Přichystal
email: Jiri.Prichystal@seznam.cz
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

# ------------------- Funkce -------------------

def get_soup(url):
    """Vrátí BeautifulSoup objekt pro danou URL."""
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Chyba při stahování stránky: {e}")
        sys.exit(1)
    return BeautifulSoup(r.text, "html.parser")


def extract_td_by_headers(soup, *headers):
    """Vrátí všechny td prvky, které mají některý z uvedených headers."""
    tds = []
    for h in headers:
        tds.extend(soup.select(f'td[headers="{h}"]'))
    return tds


def get_parties(detail_soup):
    """Vrátí seznam názvů stran pro hlavičku CSV."""
    parties_td = extract_td_by_headers(detail_soup, "t1sa1 t1sb2", "t2sa1 t2sb2")
    return [td.text.strip() for td in parties_td if td.text.strip() != "-"]


def scrape_obec(row, base_url, parties_len):
    """Zpracuje detail obce a vrátí seznam hodnot pro CSV."""
    cells = row.find_all("td")
    if not cells or not cells[0].find("a"):
        return None

    number = cells[0].text.strip()
    name = cells[1].text.strip()
    detail_url = base_url + cells[0].find("a")["href"]

    detail_soup = get_soup(detail_url)

    # základní info: voliči, obálky, platné hlasy
    numbers_td = extract_td_by_headers(detail_soup, "sa2", "sa3", "sa6")
    numbers = [td.text.strip().replace("\xa0", "") if td else "0" for td in numbers_td]
    volici = numbers[0] if len(numbers) > 0 else "0"
    obalky = numbers[1] if len(numbers) > 1 else "0"
    platne = numbers[2] if len(numbers) > 2 else "0"

    # hlasy pro strany
    votes_td = extract_td_by_headers(detail_soup, "t1sa2 t1sb3", "t2sa2 t2sb3")
    votes = []
    for td in votes_td:
        text = td.text.strip().replace("\xa0", "")
        votes.append(text if text != "-" else "0")

    # doplnit nuly, pokud počet hlasů nesedí s hlavičkou
    if len(votes) < parties_len:
        votes += ["0"] * (parties_len - len(votes))
    elif len(votes) > parties_len:
        votes = votes[:parties_len]

    return [number, name, volici, obalky, platne] + votes


def scrape_okres(url, output_file):
    """Projde všechny tabulky okresu a zapíše výsledky do CSV."""
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    soup = get_soup(url)

    # všechny tabulky s obcemi
    tables = soup.find_all("table", class_="table")
    rows = []
    for table in tables:
        rows.extend(table.find_all("tr")[2:])  # přeskočit hlavičku

    # Hlavička CSV podle první obce
    first_link = base_url + rows[0].find("a")["href"]
    detail_soup = get_soup(first_link)
    parties = get_parties(detail_soup)
    header = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + parties

    # otevření CSV a zápis dat
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for row in rows:
            data = scrape_obec(row, base_url, len(parties))
            if data:
                writer.writerow(data)

    print(f"Hotovo! Data byla uložena do {output_file}")


# ------------------- Hlavní program -------------------

def main():
    if len(sys.argv) != 3:
        print("Použití: main.py <vstupni_url> <vystupni_soubor.csv>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]
    scrape_okres(url, output_file)


if __name__ == "__main__":
    main()
