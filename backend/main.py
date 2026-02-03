from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "despesas_agregadas.csv")

def load_data():
    if not os.path.exists(DATA_PATH): return pd.DataFrame()
    return pd.read_csv(DATA_PATH, dtype={'CNPJ': str})

@app.get("/api/estatisticas")
def get_stats():
    df = load_data()
    if df.empty: return {"total_geral": 0, "media_nacional": 0, "total_ops": 0, "top_5": []}
    
    # Agrupa para o Dashboard não mostrar nomes repetidos
    agg_df = df.groupby(['CNPJ', 'RAZAO_SOCIAL', 'UF'])['VALOR'].sum().reset_index()
    
    return {
        "total_geral": float(agg_df['VALOR'].sum()),
        "media_nacional": float(agg_df['VALOR'].mean()),
        "total_ops": int(agg_df['CNPJ'].nunique()),
        "top_5": agg_df.groupby('RAZAO_SOCIAL')['VALOR'].sum().nlargest(5).reset_index().to_dict(orient='records')
    }

@app.get("/api/operadoras")
def get_operadoras(page: int = 1, search: str = ""):
    df = load_data()
    if df.empty: return {"data": [], "metadata": {"total": 0}}

    # Consolida antes de paginar
    df = df.groupby(['CNPJ', 'RAZAO_SOCIAL', 'UF'])['VALOR'].sum().reset_index()

    if search:
        s = search.upper()
        df = df[df['RAZAO_SOCIAL'].str.contains(s, na=False) | df['CNPJ'].str.contains(s, na=False)]

    start = (page - 1) * 10
    return {
        "data": df.iloc[start:start+10].to_dict(orient='records'),
        "metadata": {"total": len(df), "page": page}
    }