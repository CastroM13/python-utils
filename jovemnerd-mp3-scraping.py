from requests import get
from bs4 import BeautifulSoup

noticias = get('https://jovemnerd.com.br/nerdcast/')
retorno = []
if noticias:
  page = BeautifulSoup(noticias.content, 'html.parser')
  noticiasFormatadas = page.find_all("article", "")
  for noticia in noticiasFormatadas:
    link = get(noticia.find("a")['href'])
    filter = BeautifulSoup(link.content, 'html.parser')
    results = filter.find_all("button", "play-podcast button-default -primary")
    for result in results:
      print(result["data-podcast-url"])