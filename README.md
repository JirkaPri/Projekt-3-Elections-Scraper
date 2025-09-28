# Projekt: Webscraping výsledků voleb

## Popis

Tento skript stáhne výsledky voleb pro zadaný okres z [volby.cz](https://www.volby.cz) a uloží je do CSV souboru.  
CSV obsahuje:

- Kód obce  
- Název obce  
- Počet voličů  
- Vydané obálky  
- Platné hlasy  
- Hlasy pro všechny kandidující strany

---

## Instalace

1. **Vytvoření virtuálního prostředí:**
```bash python -m venv .venv ```

2. **Aktivace virtuálního prostředí:**

- Windows: ```bash .venv\Scripts\activate```

- Linux/Mac: ```bash source .venv/bin/activate```

3. **Instalace potřebných knihoven:**

```bash pip install -r requirements.txt```

4. **Spuštění skriptu**

```bash python main.py <url_okresu> <vystupni_soubor.csv>```

5. **Příklad vytvoření výsledného CSV souboru**

```bash python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102" vysledky_olomouc.csv```

- <url_okresu> – odkaz na stránku okresu z volby.cz
- <vystupni_soubor.csv> – název výstupního souboru CSV, kam se uloží výsledky

---

## Struktura skriptu

main.py – hlavní skript

Funkce:

- get_soup(url) – stáhne HTML a vrátí BeautifulSoup objekt
- extract_td_by_headers(soup, *headers) – vrátí všechny td prvky podle atributu headers
- get_parties(detail_soup) – získá názvy politických stran
- scrape_obec(row, base_url, parties_len) – zpracuje jednu obec a vrátí seznam hodnot
- scrape_okres(url, output_file) – projde všechny obce okresu a uloží výsledky do CSV

--- 

## Další poznámky ke skriptu

- Pokud uživatel nezadá správný počet argumentů, skript se zastaví a vypíše zprávu s instrukcemi.
- Skript je univerzální a funguje pro všechny okresy dostupné na volby.cz (Volby do PS 2017 - https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)
- CSV soubor bude obsahovat kompletní seznam obcí a všechny kandidující strany.
