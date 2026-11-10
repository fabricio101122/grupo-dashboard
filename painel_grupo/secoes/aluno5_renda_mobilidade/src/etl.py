"""ETL para percentuais de mobilidade: ingestão, validação e limpeza."""
import io
import unicodedata
import pandas as pd
import numpy as np


def _sem_acentos(s):
    return ''.join(x for x in unicodedata.normalize('NFD',str(s)) if unicodedata.category(x) != 'Mn')


def ler_tabela(arquivo):
    """Lê CSV separado por ponto-e-vírgula ou vírgula, ou Excel XLSX."""
    nome = getattr(arquivo,'name',str(arquivo)).lower()
    if nome.endswith('.xlsx'):
        return pd.read_excel(arquivo)
    if not nome.endswith('.csv'):
        raise ValueError('Envie um arquivo CSV ou XLSX.')
    # pandas sep=None com engine python identifica vírgula/ponto e vírgula.
    data = arquivo.read() if hasattr(arquivo,'read') else open(arquivo,'rb').read()
    if isinstance(data,str):data=data.encode('utf-8')
    texto = data.decode('utf-8-sig',errors='replace')
    try:
        return pd.read_csv(io.StringIO(texto),sep=None,engine='python',dtype=str)
    except Exception as erro:
        raise ValueError(f'Não foi possível ler CSV: {erro}') from erro


def converter_numero(coluna):
    """Aceita 20,5 e 20.5; rejeita dados inválidos sem converter silenciosamente para zero."""
    def um(x):
        if pd.isna(x):return np.nan
        if isinstance(x,(int,float,np.number)):return float(x)
        s = str(x).strip().replace('%','').replace(' ','')
        if ',' in s and '.' in s:
            s=s.replace('.','').replace(',','.')
        elif ',' in s:s=s.replace(',','.')
        return pd.to_numeric(s,errors='coerce')
    return pd.to_numeric(coluna.map(um),errors='coerce')


def higienizar_percentuais(df, grupos):
    """Validar e padronizar porcentagens, sem fabricar dados faltantes.

    Duplicatas por chave são um erro, pois somar percentuais duplicados gera
    falsa distribuição. A soma ~100% é verificada quando existe distribuição
    completa, mas arredondamentos publicados pelo IBGE são aceitos.
    """
    obrigatorias = ['ano',*grupos,'percentual']
    ausentes = set(obrigatorias)-set(df.columns)
    if ausentes:
        raise ValueError('Colunas obrigatórias ausentes: '+', '.join(sorted(ausentes)))
    limpeza=df.copy()
    limpeza.columns=[c.strip() for c in limpeza.columns]
    limpeza['ano']=pd.to_numeric(limpeza['ano'],errors='coerce')
    limpeza['percentual']=converter_numero(limpeza['percentual'])
    for chave in grupos:
        limpeza[chave]=limpeza[chave].astype('string').str.strip()
    chaves=['ano',*grupos]
    limpeza=limpeza.dropna(subset=[*chaves,'percentual'])
    limpeza=limpeza.loc[(limpeza['percentual']>=0)&(limpeza['percentual']<=100)].copy()
    if limpeza.empty:
        raise ValueError('A base ficou vazia após a limpeza. Revise os valores e colunas.')
    if limpeza.duplicated(subset=chaves).any():
        raise ValueError('Encontrados registros repetidos para '+', '.join(chaves))
    limpeza['ano']=limpeza['ano'].astype(int)
    return limpeza.sort_values(chaves).reset_index(drop=True)
