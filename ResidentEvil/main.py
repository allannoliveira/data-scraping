# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

url = "https://www.residentevildatabase.com/personagens/ada-wong/"

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt',
        'cache-control': 'max-age=0',
        # 'cookie': '_gid=GA1.2.2053646294.1716726078; _ga_DJLCSW50SC=GS1.1.1716728866.4.1.1716728866.60.0.0; _gat_gtag_UA_29446588_1=1; _ga_D6NF5QC4QT=GS1.1.1716728866.4.1.1716728866.60.0.0; _ga=GA1.1.389382812.1714931302; FCNEC=%5B%5B%22AKsRol_ru0ue2j3GYOITxcp_wGMDQtW6akjGxPM58DEdK0OE6XnJhUr00rARtoyTUOu65uIAqvuYi5RtvDDEtw91CmahlZcG75iUX-T0wH4-n4AkCxpzfClSzPBiw76KrsorhZN6jy_FiU1fZjpM6so9-5vNzmHb5Q%3D%3D%22%5D%5D',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

def getContent(url):
    resp = requests.get(url, headers=headers)
    return resp

def getBasicInfos(soup):
    div_page = soup.find("div", class_ = "td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")
    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")

    return data

def getAparicoes(soup):
    lis = (soup.find("div", class_ = "td-page-content")
           .find("h4")
           .find_next()
           .find_all("li"))

    aparicoes = [i.text for i in lis]
    return aparicoes

def getPersonInfo(url):

    resp = getContent(url)
    if resp.status_code != 200:
        print("Não foi possivel obter dados")
        return {}

    else:
        soup = BeautifulSoup(resp.text, features="html.parser") 
        data = getBasicInfos(soup)
        data["Aparicoes"] = getAparicoes(soup)
        
        return data


def getLinks():
    url = "https://www.residentevildatabase.com/personagens"
    resp = requests.get(url, headers=headers)
    soupPersonagens = BeautifulSoup(resp.text)

    ancoras = (soupPersonagens.find("div", class_="td-page-content")
    .find_all("a"))

    links = [i["href"] for i in ancoras]
    return links
    

links = getLinks()
data = []
for i in tqdm(links):
    d = getPersonInfo(i)
    d["Link"] = i
    nome = i.split("/")[-1].replace("-", " ").title()
    d["Nome"] = nome
    data.append(d)

df = pd.DataFrame(data)

df.to_csv("dados_re.csv", index=False, sep=":")
