from requests import get
from bs4 import BeautifulSoup


def Noticias(fonte, qtd=0):
  count = 0
  if fonte == "canalrural":
    noticias = get('https://www.canalrural.com.br/noticias-da-agropecuaria/')
    retorno = []
    if noticias:
      page = BeautifulSoup(noticias.content, 'html.parser')
      noticiasFormatadas = page.find_all("div", "info")
      for noticia in noticiasFormatadas:
        retorno.append(f"Título: {noticia.find('a') and noticia.find('a')['title'] or ''}%0aData: {noticia.find(attrs={'data-hora'}) and noticia.find(attrs={'data-hora'}).text or ''}%0aLink: {noticia.find('a') and noticia.find('a')['href'] or ''}%0aDescrição: {noticia.find('p') and noticia.find('p').text or ''}")
        count +=1
        if count == qtd:
                break
    return retorno
  elif fonte == "globo":
    noticias = get('http://g1.globo.com/dynamo/natureza/rss2.xml')
    retorno = []
    if noticias:
      noticiasFormatadas = BeautifulSoup(noticias.content)
      todasNoticiasNomes = noticiasFormatadas.find_all("item")
      for noticia in todasNoticiasNomes:
        titulo = BeautifulSoup(str(noticia.find("title")), "lxml").text
        link = BeautifulSoup(str(noticia.find("guid")), "lxml").text
        try:
            data = BeautifulSoup(str(noticia.find("guid")), "html.parser").text.split("noticia/")[1][0:10]
        except IndexError:
            data = 'Sem data'
        retorno.append(f"Título: {titulo}%0aData: {data}%0aLink: {link}")
        count +=1
        if count == qtd:
                break
    return retorno

print(Noticias("canalrural", 50))