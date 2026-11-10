"""Módulo individual do Projeto Integrador Python/Matemática.

Para o app do grupo: `from modulos.renda_mobilidade import renderizar_indicador`.
O projeto carrega CSVs locais verificados do IBGE sem depender da Internet.
"""
from pathlib import Path
import io
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ..src.etl import ler_tabela, higienizar_percentuais
from ..src.estatisticas import resumo_estatistico, percentual_mais_uma_hora, soma_por_classe_modal

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'dados' / 'tratados'
IBGE_URL = 'https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/eb6833eb8d1aa7d4f77b9b38cd20fbdb.pdf'
IPEA_URL = 'https://www.ipea.gov.br/acessooportunidades/'
CATEGORIAS_TEMPO = ['Até 5 min','6 a 30 min','31 a 60 min','61 a 120 min','Mais de 120 min']
RENDA_ORDEM=['Até 1/4 SM','> 1/4 a 1/2 SM','> 1/2 a 1 SM','> 1 a 2 SM','> 2 a 3 SM','> 3 a 5 SM','> 5 SM']
RACA_ORDEM=['Branca','Preta','Parda','Amarela','Indígena']
MODOS_ORDEM=['Automóvel','Ônibus','Motocicleta','A pé','Bicicleta','Trem ou metrô','Demais meios']
TIPOS={
    'Transporte por raça':('modal_por_raca',['cor_raca','modo']),
    'Tempo por renda':('tempo_por_renda',['faixa_renda','tempo']),
    'Tempo por cidade':('tempo_por_cidade',['cidade','uf','tempo']),
    'Transporte por região':('modal_por_regiao',['regiao','modo']),
}
CORES={'Automóvel':'#2563eb','Ônibus':'#10b981','Motocicleta':'#eab308','A pé':'#a855f7','Bicicleta':'#f97316','Trem ou metrô':'#06b6d4','Demais meios':'#94a3b8',
       'Até 5 min':'#60a5fa','6 a 30 min':'#2563eb','31 a 60 min':'#10b981','61 a 120 min':'#f59e0b','Mais de 120 min':'#ef4444'}


@st.cache_data(show_spinner=False)
def carregar_base(chave):
    arquivo,_=TIPOS[chave]
    return pd.read_csv(DATA_DIR/f'{arquivo}.csv')


def formatar(num,casas=1):
    return f'{num:,.{casas}f}'.replace(',','X').replace('.',',').replace('X','.')


def plot_layout(fig,altura=400):
    fig.update_layout(
        template='plotly_white',height=altura,margin=dict(l=6,r=12,t=26,b=10),
        font=dict(family='Arial, sans-serif',size=12,color='#1e293b'),
        legend_title_text='',hoverlabel=dict(bgcolor='white',font_size=12),
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor='#ecf0f6',zerolinecolor='#d9e0ec')
    return fig


def relatorio_stat(itens):
    base=resumo_estatistico(itens['valor'])
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Média',f"{formatar(base['media'],2)}%")
    c2.metric('Mediana / Q2',f"{formatar(base['mediana'],2)}%")
    c3.metric('IQR',f"{formatar(base['iqr'],2)} p.p.")
    c4.metric('Desvio padrão',f"{formatar(base['desvio_padrao'],2)} p.p.")
    st.caption('Medidas calculadas sobre os percentuais de cada categoria observada, não sobre pessoas individuais.')
    tabela=pd.DataFrame([
        ('Nº de observações',base['n']),('Moda',(', '.join(map(lambda v:formatar(v,2),base['moda'])) if base['moda'] else 'Não há moda')),
        ('Média (%)',formatar(base['media'],2)),('Mediana / Q2 (%)',formatar(base['mediana'],2)),
        ('Q1 (%)',formatar(base['q1'],2)),('Q3 (%)',formatar(base['q3'],2)),
        ('Intervalo interquartil / IQR (p.p.)',formatar(base['iqr'],2)),
        ('Amplitude (p.p.)',formatar(base['amplitude'],2)),
        ('Variância amostral',formatar(base['variancia'],2)),
        ('Desvio padrão amostral (p.p.)',formatar(base['desvio_padrao'],2)),
        ('Limite inferior IQR (%)',formatar(base['limite_inferior'],2)),
        ('Limite superior IQR (%)',formatar(base['limite_superior'],2)),
    ],columns=['Medida','Resultado'])
    st.dataframe(tabela,hide_index=True,use_container_width=True)
    out=itens[(itens['valor']<base['limite_inferior'])|(itens['valor']>base['limite_superior'])]
    if out.empty:
        st.info('A regra 1,5 × IQR não identificou outliers na seleção atual.')
    else:
        st.warning(f"Outlier(s) pela regra 1,5 × IQR: {', '.join(out['grupo'].astype(str))}. São grupos com percentuais extremos, não pessoas com comportamentos anormais.")
        st.dataframe(out.rename(columns={'grupo':'Grupo','valor':'Percentual (%)'}),hide_index=True,use_container_width=True)
    return base


def _baixar(nome,df,rotulo):
    st.download_button(rotulo,df.to_csv(index=False).encode('utf-8-sig'),file_name=nome,mime='text/csv')


def area_renda(df):
    st.subheader('01  |  O tempo de viagem muda conforme a renda?')
    st.write('Censo 2022 · Rendimento **domiciliar per capita** (por morador) × tempo habitual de deslocamento casa–trabalho.')
    if df.empty:
        st.warning('Nenhuma faixa de renda selecionada. Ajuste o filtro na barra lateral.');return
    longa=percentual_mais_uma_hora(df,'faixa_renda')
    longa['faixa_renda']=pd.Categorical(longa['faixa_renda'],RENDA_ORDEM,ordered=True)
    longa=longa.sort_values('faixa_renda')
    a,b,c=st.columns(3)
    a.metric('Maior proporção > 1h',f"{formatar(longa['acima_uma_hora'].max())}%")
    b.metric('Menor proporção > 1h',f"{formatar(longa['acima_uma_hora'].min())}%")
    c.metric('Diferença entre extremos',f"{formatar(longa['acima_uma_hora'].max()-longa['acima_uma_hora'].min())} p.p.")
    c1,c2=st.columns([1.45,1])
    with c1:
        st.markdown('**Distribuição percentual do tempo por faixa de renda**')
        fig=px.bar(df,x='faixa_renda',y='percentual',color='tempo',category_orders={'faixa_renda':RENDA_ORDEM,'tempo':CATEGORIAS_TEMPO},color_discrete_map=CORES,labels={'faixa_renda':'Rendimento domiciliar per capita','percentual':'Porcentagem (%)','tempo':'Tempo'},barmode='stack')
        fig.update_layout(barmode='stack',xaxis_tickangle=-25,legend=dict(orientation='h',y=-0.42))
        st.plotly_chart(plot_layout(fig,480),use_container_width=True)
    with c2:
        st.markdown('**Percentual que leva mais de 1 hora**')
        fig=px.bar(longa,x='acima_uma_hora',y='faixa_renda',orientation='h',text_auto='.1f',color_discrete_sequence=['#f97316'],labels={'acima_uma_hora':'% de pessoas','faixa_renda':'Faixa de renda'})
        fig.update_layout(yaxis=dict(categoryorder='array',categoryarray=RENDA_ORDEM[::-1]))
        st.plotly_chart(plot_layout(fig,450),use_container_width=True)
    st.caption('Os percentuais somados por faixa podem diferir de 100% em até décimos por arredondamentos do IBGE.')
    with st.expander('Ver base numérica e baixar CSV tratado'):
        st.dataframe(df,hide_index=True,use_container_width=True)
        _baixar('tempo_por_renda_filtrado.csv',df,'Baixar CSV — renda')
    st.markdown('**Leitura:** os grupos com menor renda não necessariamente têm viagem longa em todos os casos. A comparação sugere desigualdade de mobilidade, mas não prova que a renda seja sua única causa.')


def area_raca(df):
    st.subheader('02  |  Quem usa carro, ônibus ou bicicleta?')
    st.write('Percentuais do **principal meio de transporte**, definido pelo meio em que a pessoa passa mais tempo para chegar ao trabalho, segundo cor ou raça.')
    if df.empty:
        st.warning('Nenhuma categoria racial selecionada.');return
    pivot=df.pivot_table(index='cor_raca',columns='modo',values='percentual',aggfunc='first',observed=True)
    def ponto(grupo,modo):
        return pivot.loc[grupo,modo] if grupo in pivot.index and modo in pivot.columns else np.nan
    c1,c2,c3=st.columns(3)
    branco_carro,p_carro=ponto('Branca','Automóvel'),ponto('Preta','Automóvel')
    preto_onibus=ponto('Preta','Ônibus')
    c1.metric('Carro · pessoas brancas',f'{formatar(branco_carro)}%' if pd.notna(branco_carro) else '—')
    c2.metric('Carro · pessoas pretas',f'{formatar(p_carro)}%' if pd.notna(p_carro) else '—')
    c3.metric('Ônibus · pessoas pretas',f'{formatar(preto_onibus)}%' if pd.notna(preto_onibus) else '—')
    st.markdown('**Meios utilizados por cor ou raça**')
    fig=px.bar(df,x='modo',y='percentual',color='cor_raca',barmode='group',category_orders={'modo':MODOS_ORDEM,'cor_raca':RACA_ORDEM},labels={'modo':'Meio principal','percentual':'Porcentagem (%)','cor_raca':'Cor ou raça'},text_auto='.1f',color_discrete_sequence=['#2563eb','#ef4444','#f59e0b','#10b981','#a855f7'])
    fig.update_layout(xaxis_tickangle=-22,legend=dict(orientation='h',y=-0.3))
    st.plotly_chart(plot_layout(fig,480),use_container_width=True)
    classes=soma_por_classe_modal(df)
    c1,c2=st.columns([1.1,.9])
    with c1:
        st.markdown('**Participação dos modos selecionados em cada grupo**')
        fig=px.bar(classes,x='cor_raca',y='percentual',color='classe',barmode='stack',category_orders={'cor_raca':RACA_ORDEM},labels={'cor_raca':'Cor ou raça','percentual':'Porcentagem (%)'},color_discrete_sequence=['#2563eb','#10b981','#f59e0b','#94a3b8'])
        fig.update_layout(legend=dict(orientation='h',y=-.25))
        st.plotly_chart(plot_layout(fig,360),use_container_width=True)
    with c2:
        st.markdown('**Mediana do percentual por meio**')
        tabela=(df.groupby('modo',as_index=False)['percentual'].median().rename(columns={'modo':'Meio','percentual':'Mediana entre grupos (%)'}).sort_values('Mediana entre grupos (%)',ascending=False))
        st.dataframe(tabela,hide_index=True,use_container_width=True)
        st.caption('Mediana entre as categorias de raça selecionadas; NÃO é a mediana dos minutos de trajeto de cada pessoa. Se alguns modos forem desmarcados, as barras não somarão 100%.')
    with st.expander('Ver base numérica e baixar CSV tratado'):
        st.dataframe(df,hide_index=True,use_container_width=True)
        _baixar('modal_por_raca_filtrado.csv',df,'Baixar CSV — raça')


def area_cidades(df):
    st.subheader('03  |  Quais cidades enfrentam trajetos mais longos?')
    st.write('Concentrações urbanas **selecionadas na apresentação oficial** do Censo 2022. Não se trata do ranking completo de todos os municípios brasileiros.')
    cidades=df[df['cidade']!='Brasil'].copy()
    if cidades.empty:
        st.warning('Nenhuma cidade disponível para as UFs selecionadas.');return
    longa=percentual_mais_uma_hora(cidades,'cidade')
    top=longa.sort_values('acima_uma_hora',ascending=False)
    c1,c2,c3=st.columns(3)
    c1.metric('Maior concentração > 1h',top.iloc[0]['cidade'])
    c2.metric('Percentual nessa cidade',f"{formatar(top.iloc[0]['acima_uma_hora'])}%")
    c3.metric('Cidades selecionadas',f"{len(top)}")
    st.markdown('**Ranking: deslocamentos superiores a 1 hora**')
    fig=px.bar(top,x='acima_uma_hora',y='cidade',orientation='h',text_auto='.1f',color='acima_uma_hora',color_continuous_scale=['#93c5fd','#2563eb','#152f63'],labels={'cidade':'Cidade','acima_uma_hora':'Trabalhadores (%)'})
    fig.update_layout(coloraxis_showscale=False,yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(plot_layout(fig,520),use_container_width=True)
    selecionar=st.selectbox('Escolha uma cidade para comparar com a referência Brasil',sorted(cidades['cidade'].unique()),index=(sorted(cidades['cidade'].unique()).index('Belo Horizonte') if 'Belo Horizonte' in cidades['cidade'].unique() else 0))
    selecionada=cidades[cidades['cidade']==selecionar]
    fig=px.bar(selecionada,x='tempo',y='percentual',category_orders={'tempo':CATEGORIAS_TEMPO},color='tempo',color_discrete_map=CORES,text_auto='.1f',labels={'tempo':'Tempo de deslocamento','percentual':'Porcentagem (%)'})
    fig.update_layout(showlegend=False)
    st.plotly_chart(plot_layout(fig,335),use_container_width=True)
    with st.expander('Tabela das cidades e CSV para download'):
        st.dataframe(cidades,hide_index=True,use_container_width=True)
        _baixar('tempo_por_cidade_filtrado.csv',cidades,'Baixar CSV — cidades')
    st.caption('Não é possível inferir do mesmo registro individual que determinada renda ou raça causa a duração do trajeto: as tabelas têm recortes separados.')


def area_regioes(df):
    st.subheader('04  |  Modo de transporte por Grande Região')
    st.write('Comparação das cinco Grandes Regiões, útil para observar padrões de transporte motorizado, coletivo e ativo.')
    if df.empty:
        st.warning('Selecione pelo menos uma região.');return
    fig=px.bar(df,x='regiao',y='percentual',color='modo',barmode='stack',labels={'regiao':'Região','percentual':'Porcentagem (%)','modo':'Meio'},color_discrete_map=CORES)
    fig.update_layout(legend=dict(orientation='h',y=-.3))
    st.plotly_chart(plot_layout(fig,490),use_container_width=True)
    table=(df.pivot_table(index='regiao',columns='modo',values='percentual',aggfunc='first').reset_index())
    st.dataframe(table,hide_index=True,use_container_width=True)
    with st.expander('Baixar dados de comparação territorial'):
        _baixar('modal_por_regiao_filtrado.csv',df,'Baixar CSV — regiões')


def area_estatistica(renda,modal,cidades,regioes):
    st.subheader('05  |  Estatística descritiva e outliers')
    st.write('Escolha um indicador numérico. **Cada observação é um grupo agregado (uma faixa, cidade ou categoria), e não uma pessoa.**')
    opcoes={
        'Viagens acima de 1h · faixas de renda':('renda',renda),
        'Viagens acima de 1h · cidades selecionadas':('cidade',cidades),
        'Uso de ônibus · cor ou raça':('raca',modal),
        'Uso de automóvel · Grandes Regiões':('regiao',regioes),
    }
    opcao=st.selectbox('Série de percentuais para calcular',list(opcoes.keys()))
    chave,df=opcoes[opcao]
    if chave=='renda':
        tabela=percentual_mais_uma_hora(df,'faixa_renda').rename(columns={'faixa_renda':'grupo','acima_uma_hora':'valor'}) if not df.empty else pd.DataFrame()
    elif chave=='cidade':
        filtro=df[df['cidade']!='Brasil'] if not df.empty else df
        tabela=percentual_mais_uma_hora(filtro,'cidade').rename(columns={'cidade':'grupo','acima_uma_hora':'valor'}) if not filtro.empty else pd.DataFrame()
    elif chave=='raca':
        tabela=df.loc[df['modo']=='Ônibus',['cor_raca','percentual']].rename(columns={'cor_raca':'grupo','percentual':'valor'})
    else:
        tabela=df.loc[df['modo']=='Automóvel',['regiao','percentual']].rename(columns={'regiao':'grupo','percentual':'valor'})
    if tabela.empty:
        st.warning('Sem dados para calcular nessa seleção. Ajuste os filtros.');return
    if len(tabela)<4:
        st.info('Menos de 4 observações: o IQR pode ser instável. Amplie os filtros para uma análise mais informativa.')
    result=relatorio_stat(tabela)
    c1,c2=st.columns([1,1.2])
    with c1:
        fig=px.box(tabela,y='valor',points='all',hover_name='grupo',labels={'valor':'Percentual (%)'},color_discrete_sequence=['#2563eb'])
        st.plotly_chart(plot_layout(fig,340),use_container_width=True)
    with c2:
        fig=px.bar(tabela.sort_values('valor'),x='grupo',y='valor',text_auto='.2f',color_discrete_sequence=['#10b981'],labels={'grupo':'Grupo','valor':'Percentual (%)'})
        fig.add_hline(y=result['media'],line_color='#f97316',line_dash='dash',annotation_text='Média')
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(plot_layout(fig,340),use_container_width=True)
    st.markdown(f"**Interpretação:** a mediana de {formatar(result['mediana'],2)}% é menos sensível a valores extremos do que a média de {formatar(result['media'],2)}%. O IQR de {formatar(result['iqr'],2)} p.p. descreve a dispersão dos 50% centrais dos grupos selecionados.")
    _baixar('estatistica_serie_selecionada.csv',tabela,'Baixar valores analisados')


def conteudo_extra():
    st.subheader('Fontes, contexto e decisões para a gestão pública')
    st.image(str(ROOT/'assets'/'mobilidade_urbana.svg'),caption='Ilustração original do projeto: ônibus, carro, bicicleta e acesso à cidade.',use_container_width=True)
    st.markdown('''
**O que os dados permitem afirmar**

O **IBGE** mostra diferenças nos tempos de deslocamento por **renda domiciliar per capita** e nos meios de transporte por **cor ou raça**. O **Ipea – Acesso a Oportunidades** amplia a discussão: não basta medir o congestionamento; é importante medir quantos empregos e serviços um morador consegue alcançar em determinado tempo.

**Recomendações para a persona do grupo (secretário de mobilidade, prefeitos e gestores):**

- Avaliar corredores de ônibus, integrações tarifárias e confiabilidade em áreas com trajetos superiores a uma hora.
- Planejar calçadas seguras, transporte de bicicleta e conexão com pontos de ônibus.
- Medir o acesso real a escolas, hospitais e empregos dos moradores dos bairros periféricos.
- Investigar os recortes de renda e raça em cada cidade antes de definir intervenções.

**Limitações:** a renda analisada é per capita do domicílio, não necessariamente do responsável pela família; dados agregados não permitem afirmar causas individuais. A afirmação de que famílias pobres gastam 'até 20% da renda com passagens' não consta dessas tabelas e **não foi utilizada** sem validação.
''')
    a,b=st.columns(2)
    with a:
        st.link_button('Ler fonte oficial — IBGE',IBGE_URL,use_container_width=True)
        st.link_button('Consultar tabela SIDRA 10332','https://sidra.ibge.gov.br/tabela/10332',use_container_width=True)
    with b:
        st.link_button('Pesquisa Acesso a Oportunidades — Ipea',IPEA_URL,use_container_width=True)
        st.link_button('Dados abertos do Ipea','https://www.ipea.gov.br/acessooportunidades/dados/',use_container_width=True)
    st.caption('Indicadores provenientes de quadros publicados pelo IBGE com uma casa decimal. Os CSVs estão no repositório para execução offline. Não há atualização automática.')


def renderizar_indicador():
    """Exibe a seção individual. Pode ser chamada pelo app integrador do grupo."""
    st.markdown('''<style>
        .block-container {padding-top: 1.55rem; max-width: 1360px;}
        .top-hero {background:linear-gradient(115deg,#0c2546 0%,#173e75 60%,#2563eb 100%);border-radius:18px;color:white;padding:28px 30px;margin-bottom:20px;}
        .top-hero small {color:#a5e6de;text-transform:uppercase;letter-spacing:.15em;font-weight:800;}
        .top-hero h1 {color:white;font-size:2rem;margin:9px 0 8px 0;line-height:1.2;}
        .top-hero p {color:#e1e9fc;margin:0;font-size:1rem;}
        div[data-testid='stMetric'] {border:1px solid #e3e9f3;background:#f8fbff;border-radius:14px;padding:13px 14px;}
        div[data-testid='stMetricLabel'] {font-size:.87rem;}
        </style>''',unsafe_allow_html=True)
    st.markdown('''<div class="top-hero"><small>Projeto Integrador · Python + Matemática</small>
    <h1>Rendimento dos Responsáveis e a Captura do Espaço Urbano</h1>
    <p>Como renda, raça e território se relacionam à mobilidade para trabalhar? · IBGE / Censo 2022 + contexto do Ipea</p></div>''',unsafe_allow_html=True)
    st.caption('Tema individual: **Transporte e Mobilidade Urbana** | Ano dos dados: **2022** | Recorte oficial de renda: **domiciliar per capita**')
    st.sidebar.header('Filtros & dados')
    st.sidebar.markdown('**Fonte padrão:** CSVs reais transcritos de gráficos oficiais do IBGE.')
    up_tipo=st.sidebar.selectbox('Base a substituir (opcional)',list(TIPOS.keys()))
    uploaded=st.sidebar.file_uploader('Enviar CSV ou XLSX no mesmo formato do modelo',type=['csv','xlsx'],help='Selecione acima a tabela correspondente ao arquivo. Use as colunas do CSV-modelo incluído no projeto.')
    dados={key:carregar_base(key).copy() for key in TIPOS}
    if uploaded is not None:
        try:
            df_up=ler_tabela(uploaded)
            dados[up_tipo]=higienizar_percentuais(df_up,TIPOS[up_tipo][1])
            st.sidebar.success(f'Base carregada: {len(dados[up_tipo])} linhas válidas.')
        except (ValueError,KeyError,TypeError,UnicodeError) as erro:
            st.sidebar.error(f'Upload rejeitado: {erro}. Foram mantidos os dados originais.')
    anos=sorted({int(y) for df in dados.values() for y in df['ano'].dropna().unique()})
    ano=st.sidebar.selectbox('Ano',anos,index=len(anos)-1)
    dados={chave:df.loc[df['ano']==ano].copy() for chave,df in dados.items()}
    racas=[r for r in RACA_ORDEM if r in dados['Transporte por raça']['cor_raca'].unique()]
    selecionada_racas=st.sidebar.multiselect('Cor ou raça',racas,default=racas)
    modos_disp=[m for m in MODOS_ORDEM if m in dados['Transporte por raça']['modo'].unique()]
    modos_escolhidos=st.sidebar.multiselect('Meios de transporte',modos_disp,default=modos_disp)
    renda_opcoes=[r for r in RENDA_ORDEM if r in dados['Tempo por renda']['faixa_renda'].unique()]
    selecionada_renda=st.sidebar.multiselect('Faixas de renda (SM)',renda_opcoes,default=renda_opcoes)
    ufs=sorted(set(dados['Tempo por cidade']['uf'].dropna())-{'BR'})
    selecionar_ufs=st.sidebar.multiselect('UF — concentrações urbanas',ufs,default=ufs)
    regioes=sorted(dados['Transporte por região']['regiao'].dropna().unique())
    selecionar_regioes=st.sidebar.multiselect('Grandes Regiões',regioes,default=regioes)
    renda=dados['Tempo por renda'].loc[dados['Tempo por renda']['faixa_renda'].isin(selecionada_renda)].copy()
    modal=dados['Transporte por raça'].loc[dados['Transporte por raça']['cor_raca'].isin(selecionada_racas)&dados['Transporte por raça']['modo'].isin(modos_escolhidos)].copy()
    cidades=dados['Tempo por cidade'].loc[dados['Tempo por cidade']['uf'].isin(selecionar_ufs)].copy()
    regiao=dados['Transporte por região'].loc[dados['Transporte por região']['regiao'].isin(selecionar_regioes)&dados['Transporte por região']['modo'].isin(modos_escolhidos)].copy()
    st.sidebar.info('UF filtra as cidades; raça, renda e região possuem recortes nacionais separados. Não existe uma tabela individual cruzando todos os filtros.')
    t_renda,t_raca,t_cidade,t_regiao,t_stat,t_extra=st.tabs(['Renda × tempo','Raça × transporte','Cidades','Regiões','Estatísticas','Conclusões e fontes'])
    with t_renda: area_renda(renda)
    with t_raca: area_raca(modal)
    with t_cidade: area_cidades(cidades)
    with t_regiao: area_regioes(regiao)
    with t_stat: area_estatistica(renda,modal,cidades,regiao)
    with t_extra: conteudo_extra()
    st.markdown('---')
    st.caption('Números que Falam | Módulo individual — preparado para futura integração ao dashboard da equipe. Dados de referência: IBGE, Censo 2022.')
