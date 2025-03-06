import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import os
from duckduckgo_search import DDGS
import time
from time import strftime
from tqdm import tqdm

URL = 'https://www.tiobe.com/tiobe-index/'
SUBPAGES_FOLDER = ''
CURRENT_TIME = time.localtime()
LAYOUT = 'page'
INDEX_LAYOUT = 'page'

def string_to_filename(string: str) -> str:
    """
    Converts a given string into a jeykyll-filename-friendly format by replacing
    certain characters and prepending the current date.

    Args:
        string (str): The input string to be converted.

    Returns:
        str: A filename-friendly string with the current date prepended.
    """
    string = string.replace('/', '-').replace('\0', '')
    return strftime("%Y-%m-%d-", CURRENT_TIME) + string

def parse_table(htmltable) -> pd.DataFrame:
    """
    Parses the HTML table and extracts relevant data such as dates, images,
    language names, and ratings.

    Args:
        htmltable (bs4.element.Tag): A BeautifulSoup Tag representing the HTML table.

    Returns:
        pd.DataFrame: A DataFrame containing the parsed data with columns for dates,
                      change image, language image, language, rating, and rating change.
    """
    parsed_url = urlparse(URL)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    data = []

    for row in htmltable.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        data.append({
            'date1': cols[0].text.strip(),
            'date2': cols[1].text.strip(),
            'change': base_url + cols[2].find('img')['src'] if cols[2].find('img') else '',
            'img': base_url + cols[3].find('img')['src'] if cols[3].find('img') else '',
            'language': cols[4].text.strip(),
            'rating': cols[5].text.strip(),
            'rating_change': cols[6].text.strip()
        })
    
    return pd.DataFrame(data)

def to_markdown(table: pd.DataFrame) -> str:
    """
    Converts the parsed table DataFrame into Markdown format by wrapping
    cell content in Markdown links and embedding image tags.

    Args:
        table (pd.DataFrame): DataFrame containing the table data.

    Returns:
        str: A Markdown formatted string representing the table.
    """
    table["img"] = table["img"].apply(lambda url: f"<img src='{url}' width='20'>")
    table["change"] = table["change"].apply(lambda url: f"<img src='{url}' width='20'>" if url else "")

    for index, row in table.iterrows():
        lang_filename = string_to_filename(row["language"])
        for index_in_row, val in enumerate(row):
            table.iat[index, index_in_row] = f"[{val}]({lang_filename}.html)"
    
    return table.to_markdown()

def generate_markdown_subpages(table: pd.DataFrame, subpages_folder: str, df_paragraphs: pd.DataFrame) -> None:
    """
    Generates subpages as markdown files for each programming language, including headers,
    images, and content generated using a DDGS chat call.

    Args:
        table (pd.DataFrame): DataFrame containing the table data.
        subpages_folder (str): The folder path where the subpages will be saved.
        df_paragraphs (pd.DataFrame): DataFrame containing paragraph data with titles and prompts.

    Returns:
        None
    """
    for language in tqdm(table["language"]):
        filename = os.path.join(subpages_folder, f"{string_to_filename(language)}.md")
        with open(filename, 'w') as file:
            file.write(f"---\nlayout: {LAYOUT}\ntitle: \"{language}\"\n---\n\n")
            file.write(f"# <img src='{table.loc[table['language'] == language].iloc[0]['img']}' width='80'> {language}\n")
            
            for _, row in df_paragraphs.iterrows():
                file.write(f"# {row['title']}\n")
                prompt = row['prompt'].format(**table.loc[table['language'] == language].iloc[0])
                
                failure_count = 0
                while True:
                    try:
                        text = DDGS().chat(prompt, model='o3-mini', timeout=200)
                        break
                    except Exception as e:
                        failure_count += 1
                        print(f"Failure attempt {failure_count}: {e}")
                        time.sleep(3)
                
                file.write(f" {text}\n")

def main() -> None:
    """
    Main function that fetches the TIOBE index page, parses the table, converts
    the table into Markdown, and writes it to an index file.

    Args:
        None

    Returns:
        None
    """
    # Define paragraphs with title and prompt format
    paragraphs = [
        ('Official website', 'Find link to the official website of {language}'),
        ('Static typing', 'Is {language} statically typed?'),
        ('Example code', 'Write an algorithm in {language} that finds a value in a binary search tree.')
    ]
    df_paragraphs = pd.DataFrame(paragraphs, columns=['title', 'prompt'])
    
    # Fetch webpage content
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    htmltable = soup.find('table', id='top20')
    
    if htmltable:
        table = parse_table(htmltable)
        # generate_markdown_subpages(table, SUBPAGES_FOLDER, df_paragraphs)
        
        table_markdown = to_markdown(table)
        with open(os.path.join(SUBPAGES_FOLDER, "index.md"), 'w') as file:
            file.write(f"---\nlayout: {INDEX_LAYOUT}\n---\n\n")
            file.write(table_markdown)

if __name__ == "__main__":
    main()
