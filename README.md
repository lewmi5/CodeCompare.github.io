# TIOBE Index Scraper

This project scrapes the [TIOBE Index](https://www.tiobe.com/tiobe-index/) webpage to extract programming language ranking data. The script parses the HTML table, converts the data into a pandas DataFrame, and then outputs it as Markdown files. These Markdown files are intended for use with Jekyll, as this site is built using the Jekyll static site generator.

## Weird choices
- I intentionally overcomplicated my code by introducing dataframes in order to get acquainted with them.
- This folder structure is required by theme for proper search engine operation operation. That is why all markdown files are in main directory.

## Features

- **Web Scraping:** Retrieves data from the TIOBE Index website.
- **Data Parsing:** Extracts table data such as dates, images, language names, ratings, and rating changes.
- **Markdown Conversion:** Converts the parsed data into Markdown tables and pages.
- **Jekyll Integration:** Generates Markdown files formatted for use with Jekyll layouts.
- **Subpage Generation:** Creates individual Markdown subpages for each language, including generated content via DuckDuckGo Search.

### Required Python Libraries

- `requests`
- `beautifulsoup4`
- `pandas`
- `duckduckgo_search`
- `tqdm`
