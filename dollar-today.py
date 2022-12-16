from lxml import html
import requests
pagina = requests.get('https://dolarhoje.com/')

dados = html.fromstring(pagina.content)

preco = dados.xpath('//*[@id="nacional"]')[0].value

print(preco)