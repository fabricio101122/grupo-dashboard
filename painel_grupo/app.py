"""Painel unificado do grupo: Números que Falam.

Rodar, dentro da pasta painel_grupo:
    pip install -r requirements.txt
    streamlit run app.py

Cada integrante tem uma pasta em secoes/ com uma função de entrada.
Este arquivo faz só três coisas: configura a página (uma única vez),
desenha o menu da barra lateral e chama a seção escolhida.
"""
import importlib

import streamlit as st

st.set_page_config(
    page_title="Números que Falam | Painel do grupo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# (rótulo no menu, módulo, função de entrada)
SECOES = [
    ("Início", "secoes.inicio", "render"),
    ("1 · Estrutura etária, sexo e raça", "secoes.aluno1_estrutura_etaria.pagina", "render"),
    ("2 · Alfabetização e deslocamento", "secoes.aluno2_alfabetizacao.pagina", "render"),
    ("3 · População indígena e mobilidade", "secoes.aluno3_indigenas.pagina", "render"),
    ("4 · Mulheres e a mobilidade do cuidado", "secoes.aluno4_mulheres_cuidado.pagina", "render"),
    ("5 · Rendimento e mobilidade urbana", "secoes.aluno5_renda_mobilidade.modulos.renda_mobilidade", "renderizar_indicador"),
]

st.sidebar.markdown("### Números que Falam")
escolha = st.sidebar.radio("Seção", [rotulo for rotulo, _, _ in SECOES], key="menu_secao")
_, modulo, funcao = next(secao for secao in SECOES if secao[0] == escolha)

# Contexto de notícias por seção. Links encontrados em busca pública; conferir o conteúdo antes da entrega.
NOTICIAS = {
    "1 · Estrutura etária, sexo e raça": [
        ("Agência Gov, out. 2023: brasileiros com 60 anos ou mais superam 32 milhões",
         "https://agenciagov.ebc.com.br/noticias/202310/brasileiros-com-60-anos-ou-mais-superam-32-milhoes-de-pessoas-mdhc-reforca-importancia-do-cuidado-e-respeito-com-essa-faixa-etaria"),
    ],
    "2 · Alfabetização e deslocamento": [
        ("IBGE Educa: O que o Censo 2022 tem a dizer sobre alfabetização?",
         "https://educa.ibge.gov.br/professores/educa-noticias/22316-o-que-o-censo-2022-tem-a-dizer-sobre-alfabetizacao.html"),
        ("Agência IBGE: Censo 2022, taxa de analfabetismo cai de 9,6% para 7,0% em 12 anos",
         "https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-denoticias/40098-censo-2022-taxa-de-analfabetismo-cai-de-9-6-para-7-0-em-12-anos-mas-desifualdades-persistem"),
    ],
    "3 · População indígena e mobilidade": [
        ("Agência Gov / IBGE, 19 dez. 2024: Censo 2022, mais da metade da população indígena vive nas cidades",
         "https://agenciagov.ebc.com.br/noticias/202412/censo-2022-mais-da-metade-da-populacao-indigena-vive-nas-cidades"),
    ],
    "4 · Mulheres e a mobilidade do cuidado": [
        ("Brasil de Fato, 11 ago. 2023: mulheres fazem trabalho doméstico por 9,6 horas a mais que os homens",
         "https://brasildefato.com.br/2023/08/11/mulheres-fazem-trabalho-domestico-por-9-6-horas-a-mais-que-os-homens-no-brasil-aponta-ibge/"),
    ],
    "5 · Rendimento e mobilidade urbana": [
        ("Acessa.com, out. 2025: mais pobres e pretos gastam mais tempo no transporte até o trabalho",
         "https://www.acessa.com/noticias/2025/10/287929-mais-pobres-e-pretos-gastam-mais-tempo-no-transporte-ate-o-trabalho-no-brasil.html"),
    ],
}

# O import acontece só ao abrir a seção: um erro numa seção não derruba as outras.
importlib.import_module(modulo).__dict__[funcao]()

if escolha in NOTICIAS:
    st.divider()
    st.subheader("Contexto em notícias")
    st.caption("Títulos encontrados em busca pública. Abra cada link para ver o texto completo.")
    for titulo, link in NOTICIAS[escolha]:
        st.markdown(f"- [{titulo}]({link})")
