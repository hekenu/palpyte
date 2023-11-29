import pandas as pd
from bs4 import BeautifulSoup
from requests import get

# URL do site a ser raspado
url = "https://p1.trrsf.com/api/musa-soccer/ms-standings-light?idChampionship=1398&idPhase=&language=pt-BR&country=BR&nav=N&timezone=BR"

# Leitura do HTML da página.
html = response.text

# Objeto para analisar o HTML.
soup = BeautifulSoup(html, "html.parser")

# Encontrar tabelas na página.
tabelas = soup.find_all('table')

# Iterar sobre as tabelas encontradas.
for i, tabela in enumerate(tabelas):
    # Dados da tabela e DataFrame
    data = []
    colunas = []

    # Nomes das colunas da tabela.
    for th in tabela.find_all('th'):
        colunas.append(th.text.strip())

    # Certificar-se de que existem colunas.
    if colunas:
        for row in tabela.find_all('tr')[1:]:  # Ignorar a primeira somente se cabeçalho.
            columns = row.find_all(['td', 'th'])
            data.append([col.text.strip() for col in columns])

        # Número de dados com o número de colunas.
        if len(colunas) != len(data[0]):
            print(f"Ajustando o número de colunas de {len(data[0])} para {len(colunas)}")
            data = [row[:len(colunas)] for row in data]

        # DataFrame com os dados e nomes das colunas.
        df = pd.DataFrame(data, columns=colunas[:len(data[0])])

        # DataFrame com os nomes reatribuídos
        print(f"\nDataFrame {i+1} - Nomes reatribuídos:")
        print(df.to_string(index=False))
    else:
        print(f"\nSem colunas encontradas na tabela {i+1}. Ignorando esta tabela.")
