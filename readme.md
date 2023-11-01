# ASPCA Plant Toxicity Web Scraping Script

This Python script uses the BeautifulSoup and Requests libraries to scrape information from the ASPCA website about plants that are toxic to cats, dogs, and horses. It provides the ability to save the scraped data in various formats such as CSV, JSON, and XLSX.

## Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- Python (version 3.x)

## Usage

1. Clone or download the repository to your local machine.

2. Open a terminal or command prompt and navigate to the project directory.

3. Install the project's dependencies by running the following command:

```shell
    pip install -r requirements.txt
```

## Run the Script

```shell
   python aspca_plant_toxicity_scraper.py
```

## Output Files Options

You can customize the script's behavior by uncommenting the following lines in the script to save the scraped data in different formats:

- To save the scraped data as a CSV file, uncomment the following line:

```python
saveToCSV(scraped_data, "scraped_data.csv")
```

- To save the scraped data as a XLSX file, uncomment the following line:

```python
saveExcel(scraped_data, "scraped_data.xlsx")
```