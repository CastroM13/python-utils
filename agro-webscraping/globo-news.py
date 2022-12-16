from requests import get
from bs4 import BeautifulSoup

# http://g1.globo.com/dynamo/natureza/rss2.xml
# http://www.petagronomia.com/rss/all.xml

noticias = get('http://g1.globo.com/dynamo/natureza/rss2.xml')
# print(noticias.content)

if noticias:
  noticiasFormatadas = BeautifulSoup(noticias.content)
  todasNoticiasNomes = noticiasFormatadas.find_all("item")
  for noticia in todasNoticiasNomes:
    titulo = BeautifulSoup(str(noticia.find("title")), "lxml").text
    link = BeautifulSoup(str(noticia.find("guid")), "lxml").text
    desc = BeautifulSoup(str(noticia.find("description")), "lxml").text
    print("Título: " + titulo)
    print("Link: " + link)
    print("Descrição: " + ''.join(desc.split(']]>', 1)))