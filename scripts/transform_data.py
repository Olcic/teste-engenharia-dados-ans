import pandas as pd
import re
import os
import requests
import io
from unidecode import unidecode

DATA_DIR = '../data'

def limpar_texto(texto):
    if pd.isna(texto): return "NAO INFORMADO"
    return unidecode(str(texto)).strip().upper()

def run_transform():
    print(" Iniciando Transformação Sincronizada...")
    arquivo_saida = f'{DATA_DIR}/despesas_agregadas.csv'
    
    # 1. Carga
    df_fin = pd.read_csv(f'{DATA_DIR}/consolidado_despesas.csv', dtype={'REG_ANS': str})
    url_cad = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
    res = requests.get(url_cad, timeout=30)
    df_cad = pd.read_csv(io.BytesIO(res.content), sep=';', encoding='latin1', dtype=str)
    df_cad.columns = [unidecode(str(c)).strip().upper().replace(' ', '_') for c in df_cad.columns]

    # 2. Mapeamento
    col_reg = next((c for c in df_cad.columns if 'REGISTRO' in c and 'DATA' not in c), 'REGISTRO_OPERADORA')
    col_razao = next((c for c in df_cad.columns if 'RAZAO' in c and 'SOCIAL' in c), 'RAZAO_SOCIAL')
    col_cnpj = next((c for c in df_cad.columns if 'CNPJ' in c), 'CNPJ')
    col_uf = next((c for c in df_cad.columns if 'UF' in c), 'UF')

    # 3. Limpeza Profunda
    df_cad[col_razao] = df_cad[col_razao].apply(limpar_texto)
    df_cad[col_uf] = df_cad[col_uf].apply(limpar_texto)
    df_cad[col_cnpj] = df_cad[col_cnpj].str.replace(r'\D', '', regex=True).str.zfill(14)

    # 4. Join
    df_merged = pd.merge(df_fin, df_cad, left_on='REG_ANS', right_on=col_reg, how='left')
    df_merged['VALOR'] = pd.to_numeric(df_merged['VALOR'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)

    # 5. Agrupamento (MANTENDO ANO E TRIMESTRE PARA O SQL)
    print(" Agregando dados para suporte a Queries SQL...")
    final = df_merged.groupby([col_cnpj, col_razao, col_uf, 'ANO', 'TRIMESTRE']).agg({'VALOR': 'sum'}).reset_index()
    final.columns = ['CNPJ', 'RAZAO_SOCIAL', 'UF', 'ANO', 'TRIMESTRE', 'VALOR']
    
    try:
        final.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')
        print(f" Arquivo pronto para Dashboard e SQL: {arquivo_saida}")
    except PermissionError:
        print(" Feche o arquivo CSV antes de rodar o script!")

if __name__ == "__main__":
    run_transform()