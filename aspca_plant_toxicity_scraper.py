# Import necessary libraries
import csv
from math import ceil
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json

base_url = (
    "https://www.aspca.org/pet-care/animal-poison-control/toxic-and-non-toxic-plants"
)

items_per_page = 15
total_items = 1028

# Calculate the total number of pages
total_pages = ceil(total_items / items_per_page)

response = requests.get(base_url)


def scrapePage(url):
    scraped_data = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        row_content = soup.find_all("div", class_="views-row")

        links = []
        for row in row_content:
            item_link = row.find("a").get("href")
            links.append("https://www.aspca.org" + item_link)

        for link in links:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, "html.parser")
            name = soup.find("h1").text
            additional_names = None
            additional_name_pane = soup.find(
                "div", class_="field-name-field-additional-common-names"
            )
            if additional_name_pane:
                additional_names_values = additional_name_pane.find(
                    "span", class_="values"
                )
                if additional_names_values:
                    additional_names = additional_names_values.text

            scientific_names = None
            scientific_name_pane = soup.find(
                "div", class_="field-name-field-scientific-name"
            )
            if scientific_name_pane:
                scientific_name_values = scientific_name_pane.find(
                    "span", class_="values"
                )
                if scientific_name_values:
                    scientific_names = scientific_name_values.text

            family_names = None
            family_name_pane = soup.find("div", class_="field-name-field-family")
            if family_name_pane:
                family_name_values = family_name_pane.find("span", class_="values")
                if family_name_values:
                    family_names = family_name_values.text

            toxic = None
            nonToxic = None
            nontoxicity_status_pane = soup.find(
                "div", class_="field-name-field-non-toxicity"
            )
            if nontoxicity_status_pane:
                non_toxic_status = nontoxicity_status_pane.find("span", class_="values")
                if non_toxic_status:
                    nonToxic = non_toxic_status.text

            toxicity_status_pane = soup.find("div", class_="field-name-field-toxicity")
            if toxicity_status_pane:
                toxic_status = toxicity_status_pane.find("span", class_="values")
                if toxic_status:
                    toxic = toxic_status.text
            data = {
                "name": name,
                "additional_names": additional_names,
                "family_names": family_names,
                "scientific_names": scientific_names,
                "toxic": toxic,
                "non_toxic": nonToxic,
            }
            scraped_data.append(data)

    return scraped_data


scraped_data = []
for page_number in range(total_pages):
    url = base_url
    if page_number != 0:
        url = base_url + "?page=" + str(page_number)
    data = scrapePage(url)
    scraped_data = [*scraped_data, *data]


# Save to a CSV file
def saveToCSV(data, csv_filename):
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = scraped_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data[0]:
            writer.writerow(row)


# saveToCSV(scraped_data, "scraped_data.csv")


# Save in a XLSX file
def saveExcel(data, xlxs_filename):
    df = pd.DataFrame(data)
    df.to_excel(xlxs_filename, index=False)


# saveExcel(scraped_data, "scraped_data.xlsx")


# Save to JSON file
def saveToJSON(data, json_filename):
    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


saveToJSON(scraped_data, "scraped_data.json")
