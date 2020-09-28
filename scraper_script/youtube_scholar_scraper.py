# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#import import_ipynb
import selenium
from selenium import webdriver
import re
from bs4 import BeautifulSoup
import random
import time
import pandas as pd
import datetime
import nltk


# %%
driver = webdriver.Chrome('C:/Users/DjiovanniJonas/Desktop/artigo youtube dados/chromedriver')


# %%
# key word
key_words = [
    'youtube AND política',
    'youtube AND comunicação',
    'youtube AND debate',
    'youtube AND comunicação política',
    'youtube AND ciência política',
    'youtube AND participação política',
    'youtube AND debate online',
    'youtube AND debate político',
    'youtube AND eleição',
    'youyube AND campanha política'
]


# %%
a = 'youtube AND política OR youtube AND comunicação OR youtube AND debate OR youtube AND comunicação política OR youtube AND ciência política OR youtube AND participação política OR youtube AND debate online OR youtube AND debate político OR youtube AND eleição OR youtube AND campanha política'
a = re.sub('\s+', '+', a)
a


# %%
#rodar antes do write grids
def getListFromGrid(soup):
    artigos = []
    elements = soup.findAll("div", {"class":"gs_r gs_or gs_scl"})
    for element in elements:
        # title
        try:
            title = element.find("h3", {"class":"gs_rt"})
            title_text = title.text
        except:
            title_text = "NA"
        
        # title_url
        try:
            title_url = title.find("a", href=True)
            title_url = title_url["href"]
        except:
            title_url = "NA"
        
        # doc_url
        try:
            document_url = element.find("div", {"class":"gs_ggs gs_fl"})
            document_url = document_url.find("a", href=True)
            document_url = document_url["href"]
        except:
            document_url = "NA"

        # green_line
        try:
            green_line = element.find("div", {"class":"gs_a"})
            green_line.text # .text
        except:
            green_line = "NA"

        # resume
        try:
            abstract = element.find("div", {"class":"gs_rs"})
            abstract_text = abstract.text
        except:
            abstract_text = "NA"

        artigos.append({"title":title_text,
                        "title_url":title_url,
                        "doc_url":document_url,
                        "green_line":green_line,
                        "abstract":abstract_text})

    return artigos


# %%
# esse aqui

#
url = 'https://scholar.google.com.br/scholar?start={}&q=youtube+AND+política+OR+youtube+AND+comunicação+OR+youtube+AND+debate+OR+youtube+AND+comunicação+política+OR+youtube+AND+ciência+política+OR+youtube+AND+participação+política+OR+youtube+AND+debate+online+OR+youtube+AND+debate+político+OR+youtube+AND+eleição+OR+youtube+AND+campanha+política&btnG='
driver = webdriver.Chrome('C:/Users/DjiovanniJonas/Desktop/artigo youtube dados/chromedriver')

grids = []
# FIRST
driver.get('https://scholar.google.com.br/')
time.sleep(13)
driver.get(url.format(0))
time.sleep((random.random()*10)/3)
grid = driver.find_element_by_css_selector("#gs_res_ccl_mid")
grids.append(grid.get_attribute("innerHTML"))
time.sleep((random.random()*10)/2)
#/ FIRST

nResults = driver.find_element_by_css_selector("#gs_ab_md > div")
nResults = nResults.text
nResults = nResults.split("results")[0]
nResults = [e for e in nResults if e.isdigit()]
nResults = "".join(nResults).strip()
nResults = round((int(nResults) + 10)/10)
print(nResults)
for i in range(1, 100):

    driver.get(url.format(i*10))
    time.sleep((random.random()*10)/2)

    grid = driver.find_element_by_css_selector("#gs_res_ccl_mid")
    grids.append(grid.get_attribute("innerHTML"))
    time.sleep((random.random()*10)/2)

    print(i*10)

# write grids
for i in range(len(grids)):
    file = open("C:/Users/DjiovanniJonas/Desktop/artigo youtube dados/{}.html".format(i), "w+")
    file.write(grids[i])
    file.close()# grids to lists
artigos = []
for grid in grids:
    grid = BeautifulSoup(grid)
    grid_list = getListFromGrid(grid)
    artigos.extend(grid_list)# lists to DF
papers_df = pd.DataFrame(data={
    "title_text":[e["title"] for e in artigos],
    "title_url":[e["title_url"] for e in artigos],
    "green_line":[e["green_line"] for e in artigos],
    "doc_url":[e["doc_url"] for e in artigos],
    "abstract":[e["abstract"] for e in artigos]
})

now = datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y %Hh%M")
papers_df.to_excel("C:/Users/DjiovanniJonas/Desktop/artigo youtube dados/papers {}.xlsx".format(now), index=False)
new_papers_df = papers_df.loc[ ["[HTML]" not in e for e in papers_df["title_text"]]]
new_papers_df = new_papers_df.loc[ ["[CITAÇÃO]" not in e for e in new_papers_df["title_text"]]]
new_papers_df = new_papers_df.loc[ ["[BOOK]" not in e for e in new_papers_df["title_text"]]]
new_papers_df = new_papers_df.loc[ ["[LIVRO]" not in e for e in new_papers_df["title_text"]]]
new_papers_df = new_papers_df.reset_index()
new_papers_df = new_papers_df.loc[:,new_papers_df.columns != "index"]
new_papers_df


# %%
#rodar def de novo
# write grids
for i in range(len(grids)):
    file = open("C:/Users/DjiovanniJonas/Desktop/artigo youtube dados/{}.html".format(i), "wb+")
    file.write(grids[i])
    file.close()


# %%
# grids to lists
artigos = []
for grid in grids:
    grid = BeautifulSoup(grid)
    grid_list = getListFromGrid(grid)
    artigos.extend(grid_list)


# %%
# lists to DF
papers_df = pd.DataFrame(data={
    "title_text":[e["title"] for e in artigos],
    "title_url":[e["title_url"] for e in artigos],
    "green_line":[e["green_line"] for e in artigos],
    "doc_url":[e["doc_url"] for e in artigos],
    "abstract":[e["abstract"] for e in artigos]
})

#now = datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y %Hh%M")
papers_df.to_excel("C:/Users/DjiovanniJonas/Desktop/artigo youtube dados/papers.xlsx", index=False)


# %%
papers_df.to_csv("C:/Users/DjiovanniJonas/Desktop/artigo youtube dados/papers.csv", index=False)


# %%
papers_df


# %%
new_papers_df = papers_df.loc[ ["[HTML]" not in e for e in papers_df["title_text"]]]
new_papers_df = new_papers_df.loc[ ["[CITAÇÃO]" not in e for e in new_papers_df["title_text"]]]
new_papers_df = new_papers_df.loc[ ["[BOOK]" not in e for e in new_papers_df["title_text"]]]
new_papers_df = new_papers_df.loc[ ["[LIVRO]" not in e for e in new_papers_df["title_text"]]]
new_papers_df = new_papers_df.reset_index()
new_papers_df = new_papers_df.loc[:,new_papers_df.columns != "index"]
new_papers_df


# %%
titles_url = list(papers_df['title_url'])
sites_list = []
for e in titles_url:
    try:
        site = re.search(".*?\.(.*?\..*?)\.", e).group(1)
        sites_url = sites_list.append(site)
    except:
        sites_url = sites_list.append("NA")

unique_sites = list(set(sites_list))

for u in unique_sites:
    print(u)
    
print(len(unique_sites))

count_sites = {}
for u in unique_sites:
    count_sites[u] = sites_list.count(u)


# %%
keys = list(count_sites.keys())
values = list(count_sites.values())

sites_count_df = pd.DataFrame(data={"keys":keys, "values":values})
sites_count_df.sort_values('values', ascending=False)


# %%
papers_df['green_line'] = [BeautifulSoup(str(e)).text for e in papers_df['green_line']]


