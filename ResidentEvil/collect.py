# %%
import requests
from bs4 import BeautifulSoup

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '_gid=GA1.2.1155743693.1718924880; _ga_DJLCSW50SC=GS1.1.1718924879.1.1.1718924886.53.0.0; _ga_D6NF5QC4QT=GS1.1.1718924879.1.1.1718924886.53.0.0; _ga=GA1.2.316155405.1718924879; FCNEC=%5B%5B%22AKsRol_bOEmgjXuCSLJGMux1d9UJgq-Hs1z1WOJbstxTfeAhayg0-CCmYIXpPHAMsg_2eBLju9abNQba6LVKjpt8dp2ZaAsA2EZRXmdPEfAI5VheiwOBZEJSKGGYHL3UFOxSVGNPnTG4QgnqtEo_Mc4PfbIPBzlNRw%3D%3D%22%5D%5D',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp


def get_basic_infos(soup):
    div_page = soup.find('div', class_='td-page-content')
    paragrafo = div_page.find_all('p')[1]
    ems = paragrafo.find_all('em')
    data = {}
    for i in ems:
        chave, valor =i.text.split(':')
        chave = chave.strip(' ')
        data[chave] = valor.strip(' ')
    return data


def get_aparicoes(soup):
    lis = (soup.find("div", class_="td-page-content")
            .find("h4")
            .find_next()
            .find_all("li"))

    aparicoes = [i.text for i in lis]
    return aparicoes


def get_personagem_infos(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("Não foi possível obter os dados")
        return {}
    else:
        soup = BeautifulSoup(resp.text, "html.parser")
        data = get_basic_infos(soup)
        data['Aparicoes'] = get_aparicoes(soup)
        return data

def get_links():
    url = 'https://www.residentevildatabase.com/personagens/'
    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens
            .find('div', class_='td-page-content')
            .find_all('a'))

    links = [i['href'] for i in ancoras]
    return links

# %%

url = 'https://www.residentevildatabase.com/personagens/ada-wong/'

get_personagem_infos(url)

# %%

links = get_links()
data = []
for i in links:
    perso = get_personagem_infos(i)
    perso['link'] = i
    data.append(perso)
# %%
data