import pandas as pd
from bs4 import BeautifulSoup
import requests

# URL do site a ser raspado
url = "https://p1.trrsf.com/api/musa-soccer/ms-standings-light?idChampionship=1398&idPhase=&language=pt-BR&country=BR&nav=N&timezone=BR"

# Fazendo a solicitação HTTP e obtendo o HTML da página.
response = requests.get(url)
html = response.text

# Obj para analisar o HTML.
soup = BeautifulSoup(html, "html.parser")

# Encontrar tabs.
tabelas = soup.find_all('table')

# Iterar sobre tabs.
for i, tabela in enumerate(tabelas):
    # Dados tab e DataFrame
    data = []
    colunas = []

    # Nomes colunas da tab.
    for th in tabela.find_all('th'):
        colunas.append(th.text.strip())

    # Certificar existem colunas.
    if colunas:
        for row in tabela.find_all('tr')[1:]:  # Ignorar somente se cabeçalho.
            columns = row.find_all(['td', 'th'])
            data.append([col.text.strip() for col in columns])

        # Número de dados com o número de colunas.
        if len(colunas) != len(data[0]):
            print(f"Ajustando o número de colunas de {len(data[0])} para {len(colunas)}")
            data = [row[:len(colunas)] for row in data]

        # DataFrame dados e nomes colunas.
        df = pd.DataFrame(data, columns=colunas[:len(data[0])])

        # DataFrame com os nomes reatribuídos
        print(f"\nDataFrame {i+1} - Nomes reatribuídos:")
        print(df.to_string(index=False))
    else:
        print(f"\nSem colunas encontradas na tabela {i+1}. Ignorando esta tabela.")
