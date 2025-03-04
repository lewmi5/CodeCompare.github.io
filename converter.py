import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import os
from duckduckgo_search import DDGS
import time
from time import strftime
from tqdm import tqdm

url = 'https://www.tiobe.com/tiobe-index/'
subpages_folder = ''
current_time = time.localtime()
layout = 'page'
index_layout = 'page'

def string_to_filename(string):
    string = string.replace('/', '-')
    string = string.replace('\0', '')
    return strftime("%Y-%m-%d-", current_time) + string
    # return "2025-03-03-" + string

def parse_table(htmltable):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    data = []

    for row in htmltable.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        date1 = cols[0].text.strip()
        date2 = cols[1].text.strip()
        change = base_url + cols[2].find('img')['src'] if cols[2].find('img') else ''
        img = base_url + cols[3].find('img')['src'] if cols[3].find('img') else ''
        language = cols[4].text.strip()
        rating = cols[5].text.strip()
        rating_change = cols[6].text.strip()

        data.append({
            'date1': date1,
            'date2': date2,
            'change': change,
            'img': img,
            'language': language,
            'rating': rating,
            'rating_change': rating_change
        })
    table = pd.DataFrame(data)
    return table

def to_markdown(table):
    table["img"] = table["img"].apply(lambda url: f"<img src ='{url}' width ='20'>")
    table["change"] = table["change"].apply(lambda url: f"<img src ='{url}' width ='20'>" if url else "")

    for index, row in table.iterrows():
        # path_to_language_file = os.path.join(strftime('%Y'), strftime('%m'), strftime('%d'), f"{row["language"]}.html")
        for index_in_row, val in enumerate(row):
            lang_filename = string_to_filename(row["language"])
            table.iat[index, index_in_row] = f"[{val}]({lang_filename}.html)"

            # table.iat[index, index_in_row] = f"[{val}]({string_to_filename(row["language"])}.html)"

    return table.to_markdown()

def generate_markdown_subpages(table, subpages_folder, df_paragraphs):
    # if not os.path.exists(subpages_folder):
    #     os.makedirs(subpages_folder)

    for language in tqdm(table["language"]):
        with open(os.path.join(subpages_folder, f"{string_to_filename(language)}.md"), 'w') as file:
            file.write(f"---\nlayout: {layout}\ntitle: \"{language}\"\n---\n\n")
            file.write(f"# <img src='{table.loc[table['language'] == language].iloc[0]['img']}' width='80'> {language}\n")
            for index, row in df_paragraphs.iterrows():
                file.write(f"# {row['title']}\n")
                prompt = row['prompt'].format(**(table.loc[table['language'] == language].iloc[0]))
                failure = 1
                while(True):
                    try:
                        text = DDGS().chat(prompt, model='o3-mini', timeout=200)
                        # text = DDGS().text(prompt)
                        break
                    except Exception as e:
                        print(f"number of failures: {failure}")
                        failure += 1
                        time.sleep(3)

                file.write(f" {text}\n")
            file.close()

def main():
    paragraphs = [('Official website', 'find link to official website of {language}'),('Static typing', 'Is {language} statically typed?'), ('Example code', 'Write an algorithm in {language} that finds a value in a binary search tree.')]

    df_paragraphs = pd.DataFrame({'title' : [], 'prompt' : []})
    for paragraph in paragraphs:
        df_paragraphs.loc[len(df_paragraphs)] = paragraph

    text = requests.get(url)
    soup = BeautifulSoup(text.content, 'html.parser')
    htmltable = soup.find('table', id='top20')
    if htmltable:
        table = parse_table(htmltable)
        # table = table[:14]
        # generate_markdown_subpages(table, subpages_folder, df_paragraphs)
        table_markdown = to_markdown(table)
        with open(os.path.join(subpages_folder, "index.md"), 'w') as file:
            file.write(f"---\nlayout: {index_layout}\n---\n\n")
            file.write(table_markdown)

if __name__ == "__main__":
    main()
