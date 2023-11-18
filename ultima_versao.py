import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

# URL_site_raspado
url = input("Digite a URL do site a ser raspado: ")

# Abrir_URL_ler_conteúdo_HTML_página
page = urlopen(url)
html = page.read().decode("utf-8")

# Criar_um_objeto_BeautifulSoup_para_analisar_HTML
soup = BeautifulSoup(html, "html.parser")

# Encontrar_tabelas_página
tabelas = soup.find_all('table')

# Iterar_tabelas
for i, tabela in enumerate(tabelas):
    # Extrair dados da tabela e criar um DataFrame
    data = []
    colunas = []

    # Obter_nomes_colunas_tabela
    for th in tabela.find_all('th'):
        colunas.append(th.text.strip())

    # Certificar-se_de_que_existem_colunas_antes_de_tentar_extrair_dados
    if colunas:
        for row in tabela.find_all('tr')[1:]:  # Ignorar a primeira linha se for o cabeçalho
            columns = row.find_all(['td', 'th'])
            data.append([col.text.strip() for col in columns])

        # Verificar_se_o_número_de_colunas_nos_dados_é_consistente_com_o_número_de_colunas_nas colunas
        if len(colunas) != len(data[0]):
            print(f"Ajustando o número de colunas de {len(data[0])} para {len(colunas)}")
            data = [row[:len(colunas)] for row in data]

        # Criar_um_DataFrame_com_os_dados_e_atribuir_nomes_às_colunas
        df = pd.DataFrame(data, columns=colunas[:len(data[0])])

        # Exibir_o_DataFrame_com_os_nomes_reatribuídos
        print(f"\nDataFrame {i+1} - Nomes reatribuídos:")
        print(df)
    else:
        print(f"\nSem colunas encontradas na tabela {i+1}. Ignorando esta tabela.")
