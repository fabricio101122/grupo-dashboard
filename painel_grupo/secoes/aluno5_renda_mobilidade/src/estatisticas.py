"""Estatística descritiva de percentuais agregados divulgados pelo IBGE."""
import numpy as np
import pandas as pd


def resumo_estatistico(valores):
    x=pd.to_numeric(pd.Series(valores),errors='coerce').dropna().astype(float).to_numpy()
    if not len(x): raise ValueError('Não há dados numéricos para os filtros selecionados.')
    media=float(np.mean(x)); mediana=float(np.median(x))
    q1, q3=map(float,np.percentile(x,[25,75])); iqr=q3-q1
    inferior=q1-1.5*iqr; superior=q3+1.5*iqr
    vc=pd.Series(x).value_counts()
    maior=int(vc.max())
    modas=sorted(vc[vc==maior].index.tolist()) if maior > 1 else []
    extremos=x[(x<inferior)|(x>superior)]
    return {
        'n':len(x),'media':media,'mediana':mediana,'moda':modas,
        'q1':q1,'q2':mediana,'q3':q3,'iqr':iqr,
        'amplitude':float(np.max(x)-np.min(x)),
        'variancia':float(np.var(x,ddof=1)) if len(x)>1 else 0.0,
        'desvio_padrao':float(np.std(x,ddof=1)) if len(x)>1 else 0.0,
        'limite_inferior':inferior,'limite_superior':superior,
        'outliers':extremos.tolist(),
        'minimo':float(np.min(x)),'maximo':float(np.max(x)),
    }


def percentual_mais_uma_hora(df, coluna):
    """Retorna soma em p.p. de 61–120 e >120 min por categoria.
    Os totais não são ponderados entre cidades/faixas, pois faltam os n's."""
    filtro=df.loc[df['tempo'].isin(['61 a 120 min','Mais de 120 min'])]
    return (filtro.groupby(coluna,as_index=False,sort=False)['percentual']
                  .sum().rename(columns={'percentual':'acima_uma_hora'}))


def soma_por_classe_modal(df):
    classes={
        'Automóvel':'Individual motorizado','Motocicleta':'Individual motorizado',
        'Ônibus':'Transporte coletivo','Trem ou metrô':'Transporte coletivo',
        'A pé':'Transporte ativo','Bicicleta':'Transporte ativo',
        'Demais meios':'Outros','Embarcação pequena':'Outros',
    }
    data=df.copy();data['classe']=data['modo'].map(classes).fillna('Outros')
    grupo='cor_raca' if 'cor_raca' in data.columns else 'regiao'
    return data.groupby([grupo,'classe'],as_index=False)['percentual'].sum()
