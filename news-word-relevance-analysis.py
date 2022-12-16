# Importa a função get do pacote requests que efetua solicitações web.
from requests import get
# Importa a função BeautifulSoup do pacote bs4
from bs4 import BeautifulSoup

# Palavras que não serão analisadas:
illegalStatements = ['na', 'de', 'da', 'em', 'e', 'os', 'a', 'o', 'com', 'do', 'as', 'das', 'dá', 'dos', 'no', 'nas', 'nos', 'que', 'para', 'lhe', 'lá', 'uma', 'um', 'é', 'ao', 'há', 'meio', 'também', 'mais', 'sem', 'não', 'diz', 'está', 'maior', 'menor', 'até', 'à', 'ou', 'por', 'pelo', 'par', 'aos', 'como', 'às', 'são', 'suas', 'sobre', 'ser', 'fazer', 'têm', 'dele', 'ele', 'ela', 'dela', 'dar', 'mas', 'muito', 'sua', 'seu', 'seus', 'será', 'teve', 'pela', 'nesse', 'nessa', 'nesses', 'nessas', 'desse', 'desses', 'dessa', 'dessas', 'foi', 'então', 'porque', 'nesta', 'neste', 'todo', 'todos', 'toda', 'todas', 'quem', 'eram', 'aqui', 'numa', 'uso', 'usar', 'outro', 'outra', 'outros', 'outras', 'se', 'for', 'usou', 'ainda', 'antes', 'este', 'esta', 'está', 'estão', 'deles', 'delas', 'podem', 'pode']
# Mostra os detalhes da notícia:
showNews = True
# Qual o máximo de análises serão efetuadas:
analysisCount = 5
# Quantas vezes uma palavra precisa aparecer para ela ser analisada:
relevanceThreshold = 4
# O tamanho mínimo de uma palavra pra ela ser analisada por relevância:
minWordSize = 3

# Preenche a variável 'site' com o corpo não filtrado do site 'https://g1.globo.com/'
site = get('https://g1.globo.com/')
# Se a requisição da página fracassar (Falta de internet, Site caiu e etc) o Script não roda e evita crashes.
if site:
  # Preenche a variável 'page' com a execução da função BeautifulSoup que tornará a página legível pelos métodos internos da extensão.
  # Esta função efetua uma análise da página e separa os elementos para permitir uma busca pelas tags e propriedades.
  page = BeautifulSoup(site.content, 'html.parser')
  # Preenche a variável 'listaNoticias' com a função find_all que gera uma lista com todos os elementos 'div' da página que possuírem a classe 'feed-post-body'.
  listaNoticias = page.find_all("div", "feed-post-body")
  # Itera na lista de elementos div de Notícia para executar outras funções em cada uma das Notícias.
  for item in listaNoticias:
    # Se a variável 'showNews' estiver como verdadeira, ele mostrará mais detalhes da notícia na análise, se não mostrará apenas o Título e o Link.
    if showNews:
      # Imprime várias informações na tela, filtrando pelo método find que
      # encontra um elemento e sua classe na página e extrai o valor de texto se o mesmo existir e não for nulo.
      chapeu = item.find('span', 'feed-post-header-chapeu')
      titulo = item.find('a', 'feed-post-link gui-color-primary gui-color-hover')
      link = item.find('a', 'feed-post-link gui-color-primary gui-color-hover')['href']
      topico = item.find('span', 'feed-post-metadata-section')
      print('Chapéu:', chapeu.text if chapeu else None)
      print('Título:', titulo.text if titulo else None)
      print('Link:', link if link and titulo.has_attr('href') else None)
      print('Tópico:', topico.text if topico else None)
    # Busca garantir que a âncora da página possui o link da notícia.
    if titulo.has_attr('href'):
      # Se a âncora possuir o link, faz a requisição de dados da página da notícia e preenche a variável 'noticia'
      noticia = get(link)
      # Se a notícia existir e não for nula, continua.
      if noticia:
        # Preenche a variável 'noticiaFiltrada' com a execução da função BeautifulSoup que tornará a página legível pelos métodos internos da extensão.
        noticiaFiltrada = BeautifulSoup(noticia.content, 'html.parser')
        # Imprime o Subtítulo da notícia, buscando a tag h2 com a classe correta caso esta existir
        print('Subtítulo:', noticiaFiltrada.find('h2', 'content-head__subtitle').text if noticiaFiltrada.find('h2', 'content-head__subtitle') else None) if showNews else None
        # Inicializa uma variável com uma quebra de linha para preencher e alinhas corretamente o conteúdo da notícia.
        todasLinhas = '\n'
        # Itera a noticia, filtrando apenas os parágrafos que contém os textos importantes pra notícia.
        for linha in noticiaFiltrada.find_all('p', 'content-text__container'):
          # Preenche a variável todasLinhas sem apagar o que já está presente adicionando as linhas da notícia e uma quebra de linha para alinhar corretamente.
          todasLinhas = todasLinhas + linha.text + str('\n')
        # Imprime a notícia inteira
        print('Notícia:', todasLinhas) if showNews else None
        # Inicializa uma lista vazia chamada obj que possuirá o texto, onde está localizado, quantas vezes repete e a frase de que o origina.
        obj = []
        # Inicializa uma lista vazia chamada used para preencher com os termos que já foram adicionados para evitar a repetição
        used = []
        # Preenche uma lista com todas as palavras separando as por espaço.
        palavrasSeparadas = todasLinhas.split(" ")
        # Itera na lista de palavrasSeparadas e executa o bloco que preenche as palavras que serão analisadas.
        for i in palavrasSeparadas:
          # Se a palavra tiver pelo menos o tamanho mínimo e não tiver sido analisada e não for uma palavra proibida pela lista inicial executa a análise.
          if len(i) >= minWordSize and not i in used and not i in illegalStatements:
              # Adiciona a palavra na lista de palavras já analisadas.
              used.append(str(i))
              # Adiciona na lista de objetos analisados um Dicionário com os valores analisados.
              obj.append({
                # Adiciona o texto da palavra.
                "value": str(i),
                # Adiciona o índice de onde a palavra aparece pela primeira vez na frase.
                "index": todasLinhas.find(str(i)),
                # Adiciona a quantidade de vezes que a palavra aparece.
                "count": palavrasSeparadas.count(str(i)),
                # Adiciona uma lista de frases em que a palavra foi usada através de um filtro que executa
                # uma função anônima (Lambda) que confere numa lista de frases separadas por '.' se a palavra está presente.
                "context": list(filter(lambda x: str(i) in x, todasLinhas.split(".")))
                })
        # Ordena todas as palavras pelas que mais aparecem primeiro e limita o preenchimento pelo limite de palavras analisadas.
        result = list(reversed(sorted(obj, key=lambda d: d['count'])))[:analysisCount]
        # Imprime um elemento gráfico na tela para ajudar na organizaçao das análises.
        print("Análise: \n---------------------------------------------------------")
        # Garante que a lista de palavras não estará vazia.
        if len(result) > 0:
          # Se estiver no modo simples de descrição, imprime apenas o Título e o Link da notícia junto com a análise.
          print('Título:', titulo.text if titulo else None) if not showNews else None
          print('Link:', link if titulo else None) if not showNews else None
          # Itera sobre a lista de palavras para denotar cada análise individual.
          for analysis in result:
            # Se a quantidade de vezes que a palavra aparece for maior que o limite míninmo, executa o bloco seguinte.
            if analysis['count'] >= relevanceThreshold:
              # Preenche a palavra e a quantidade de vezes que ela aparece para poder imprimí-la.
              value = analysis['value']
              count = analysis['count']
              # Imprime a palavra e a quantidade de vezes que ela aparece
              print(f'A palavra "{value}" aparece {count} vezes.')
              # Enumera o a lista de palavras e itera sobre ela iniciando no índice 1.
              for idx, frase in enumerate(analysis['context'], start=1):
                # Imprime o índice, a frase em que a palavra apareceu, removendo quebras de linha e espaços desnecessários à direita e esquerda do texto.
                print(f'{idx}.', frase.replace('\n', ' ').replace('\r', '').rstrip().lstrip())
              # Imprime um elemento gráfico na tela para ajudar na organizaçao das análises.
              print('---------------------------------------------------------')