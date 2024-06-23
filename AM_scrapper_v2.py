import requests
import pandas
import time
from bs4 import BeautifulSoup

# Leio o .csv com o pandas e uso a primeira coluna como índice
dtype = {"movieId": str, "imdbId": str, "tmdbId": str}
df = pandas.read_csv('links.csv', index_col='movieId', dtype=dtype)

# Construo a URL, faço as requisições, salvo o html e faço o parse do html.
for index, row in df.iterrows():
    time.sleep(0.5) # 2 páginas por segundo
    url = 'https://www.imdb.com/title/tt' + row['imdbId'] + '/fullcredits?ref_=tt_ov_st_sm'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    with open("C:\\Users\\romul\\scrapped_html\\" + index + ".html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    file.close()


    # Faz o scrapping do conteúdo.
    # Eu busco pelo id do header relevante, pois pode haver filme que não traga tal informação.
    # Se o header não for encontrado, "selection" vale "none" e o "else" é executado.
    # Havendo o header, o próximo item do html é a tabela que tem os dados que quero.
    # Nesse caso, o "if" é executado, buscando todos os "tds" relevantes um a um.
    # Atenção para os tds, pois os busco pela classe e nem todos são "name".
    # Também é possível existir mais de um "td" sem classe no "cast" com "a" vazio.
    # Para evitar esse e outros problemas, verifico sempre se "a" existe mesmo.

    director = ""
    writer = ""
    cast = ""
    producer = ""

    # director
    selection = soup.find("h4", {"id": "director"})
    if(selection):
        cells = selection.findNext('table').find_all('td', class_='name')
        for cell in cells:
            if(cell.find('a')):
                if director: # se já tem texto, adiciono separador
                    director += "|"
                director += cell.find('a').get_text().strip() # adiciono o texto
    else:
        director = "NOT_FOUND"
    print(director)

    # writer
    selection = soup.find("h4", {"id": "writer"})
    if(selection):
        cells = selection.findNext('table').find_all('td', class_='name')
        for cell in cells:
            if(cell.find('a')):
                if writer:
                    writer += "|"
                writer += cell.find('a').get_text().strip()
    else:
        writer = "NOT_FOUND"
    print(writer)

    # cast
    selection = soup.find("h4", {"id": "cast"})
    if(selection):
        cells = selection.findNext('table').find_all('td', class_='')
        for cell in cells:
            if(cell.find('a')):
                if cast:
                    cast += "|"
                cast += cell.find('a').get_text().strip()
    else:
        cast = "NOT_FOUND"
    print(cast)

    # producer
    selection = soup.find("h4", {"id": "producer"})
    if(selection):
        cells = selection.findNext('table').find_all('td', class_='name')
        for cell in cells:
            if(cell.find('a')):
                if producer:
                    producer += "|"
                producer += cell.find('a').get_text().strip()
    else:
        producer = "NOT_FOUND"
    print(producer)

    # Faço append dos dados num arquivo csv

    line    = index + "," \
            + director + "," \
            + writer + "," \
            + cast + "," \
            + producer + "\n"
    f = open('scrapped_data.csv', 'a', encoding="utf-8")
    f.write(line)
    f.close()


