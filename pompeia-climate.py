from requests import get
from bs4 import BeautifulSoup

site = get('https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/519/pompeia-sp')
if site:
  page = BeautifulSoup(site.content, 'html.parser')
  siteFormatado = page.find_all("div", "_flex _align-center _align-start-sm _flex-column-sm _margin-r-10")
  for item in siteFormatado:
    print(item.find('p').text)
    print('Temperatura Mínima: ', item.findAll('span')[0].text, "C")
    print('Temperatura Máxima: ', item.findAll('span')[1].text, "C")
