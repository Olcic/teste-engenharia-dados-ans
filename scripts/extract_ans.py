import pandas as pd
import requests
import zipfile
import io
import os
from unidecode import unidecode

DATA_DIR = '../data'
os.makedirs(DATA_DIR, exist_ok=True)
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# URLs Reais dos últimos 3 trimestres disponíveis (Exemplo 2025)
URLS = {
    '2025_1T': 'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2025/1T2025.zip',
    '2025_2T': 'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2025/2T2025.zip',
    '2025_3T': 'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2025/3T2025.zip'
}

def normalizar_col(col):
    return unidecode(str(col)).strip().upper().replace(' ', '_')

def extrair():
    dfs = []
    for periodo, url in URLS.items():
        print(f" Baixando {periodo}...")
        try:
            r = requests.get(url, headers=HEADERS, timeout=120)
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                csv_file = [f for f in z.namelist() if f.endswith('.csv')][0]
                with z.open(csv_file) as f:
                    df = pd.read_csv(f, sep=';', encoding='latin1', low_memory=False)
                    df.columns = [normalizar_col(c) for c in df.columns]
                    
                    # Identifica colunas essenciais
                    col_reg = next((c for c in df.columns if 'REG_ANS' in c or 'REGISTRO' in c), None)
                    col_valor = next((c for c in df.columns if 'VL_SALDO' in c), None)
                    
                    if col_reg and col_valor:
                        df_fmt = pd.DataFrame({
                            'REG_ANS': df[col_reg],
                            'VALOR': df[col_valor],
                            'ANO': periodo.split('_')[0],
                            'TRIMESTRE': periodo.split('_')[1][0]
                        })
                        dfs.append(df_fmt)
        except Exception as e:
            print(f" Erro em {periodo}: {e}")

    if dfs:
        pd.concat(dfs).to_csv(f'{DATA_DIR}/consolidado_despesas.csv', index=False)
        print(" Extração concluída.")

if __name__ == "__main__":
    extrair()