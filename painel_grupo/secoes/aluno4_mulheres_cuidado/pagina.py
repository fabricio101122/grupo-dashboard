"""Seção do Aluno 4: Mulheres e a "Mobilidade do Cuidado".

Como rodar:
    pip install -r requirements.txt
    streamlit run app.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ------------------------------------------------------------------ dados
PASTA = Path(__file__).parent
uf = pd.read_csv(PASTA / "dados/uf_horas_cuidado.csv")
regiao = pd.read_csv(PASTA / "dados/regiao_sexo_ocupacao.csv")
brasil = pd.read_csv(PASTA / "dados/brasil_serie.csv")

REGIOES = ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]


# ------------------------------------------------------- função principal
def painel(df, coluna, titulo):
    """Mostra cards, histograma, boxplot e outliers de uma coluna numérica."""
    if len(df) < 4:
        st.info("Poucos dados para este filtro (menos de 4 observações).")
        return

    s = df[coluna].to_numpy()  # vetor NumPy com os valores

    # Quartis e medidas de dispersão
    q1, q2, q3 = np.percentile(s, [25, 50, 75])
    iqr = q3 - q1

    # Moda: valor(es) mais repetido(s); se nenhum se repete, não há moda
    valores, contagens = np.unique(s, return_counts=True)
    if contagens.max() > 1:
        moda = ", ".join(str(m) for m in valores[contagens == contagens.max()])
    else:
        moda = "sem moda"

    # Cards de resumo
    linha1 = st.columns(5)
    linha1[0].metric("Média", f"{np.mean(s):.2f} h")
    linha1[1].metric("Mediana (Q2)", f"{q2:.2f} h")
    linha1[2].metric("Moda", moda)
    linha1[3].metric("Amplitude", f"{np.ptp(s):.2f} h")  # ptp = máximo - mínimo
    linha1[4].metric("Observações", len(s))
    linha2 = st.columns(5)
    linha2[0].metric("Q1", f"{q1:.2f} h")
    linha2[1].metric("Q3", f"{q3:.2f} h")
    linha2[2].metric("IQR", f"{iqr:.2f} h")
    linha2[3].metric("Variância", f"{np.var(s, ddof=1):.2f} h²")  # ddof=1: amostral
    linha2[4].metric("Desvio padrão", f"{np.std(s, ddof=1):.2f} h")

    # Gráficos
    g1, g2 = st.columns(2)
    g1.plotly_chart(px.histogram(df, x=coluna, nbins=8, title=f"Histograma: {titulo}"))
    g2.plotly_chart(px.box(df, y=coluna, points="all", title=f"Boxplot: {titulo}"))

    # Outliers: valores fora de [Q1 - 1,5*IQR ; Q3 + 1,5*IQR]
    limite_baixo = q1 - 1.5 * iqr
    limite_alto = q3 + 1.5 * iqr
    outliers = df[(s < limite_baixo) | (s > limite_alto)]
    faixa = f"{limite_baixo:.2f} a {limite_alto:.2f}"
    if outliers.empty:
        st.success(f"Nenhum outlier (faixa esperada: {faixa}).")
    else:
        st.warning(f"Outliers fora da faixa {faixa}:")
        st.dataframe(outliers, hide_index=True)


# ---------------------------------------------------------------- filtros
def render():
    st.sidebar.header("Filtros")
    ano = st.sidebar.selectbox("Ano", [2022, 2019])
    regioes = st.sidebar.multiselect("Região", REGIOES, default=REGIOES)
    ufs_disp = sorted(uf.loc[uf["ano"] == ano, "uf"].unique())
    ufs_sel = st.sidebar.multiselect("UF", ufs_disp, default=ufs_disp)
    st.sidebar.caption("Recorte por UF e região só existe para 2022.")

    # ------------------------------------------------------------- cabeçalho
    st.title("Mulheres e a “Mobilidade do Cuidado”")
    st.caption(
        "Fonte: IBGE, PNAD Contínua, Outras formas de trabalho (14 anos ou mais). "
        "Indicador: horas semanais dedicadas a afazeres domésticos e/ou cuidados de pessoas."
    )

    # Cards do Brasil
    b = brasil[brasil["ano"] == ano].set_index("sexo")["horas"]
    c = st.columns(3)
    c[0].metric("Brasil: homens", f"{b['Homens']:.1f} h" if "Homens" in b else "—")
    c[1].metric("Brasil: mulheres", f"{b['Mulheres']:.1f} h" if "Mulheres" in b else "—")
    c[2].metric("Diferença (M − H)", f"{b['Mulheres'] - b['Homens']:.1f} h" if "Mulheres" in b else "—")

    aba1, aba2, aba3, aba4 = st.tabs(["Por UF", "Homens × Mulheres", "Lacuna de gênero", "Análise"])

    # ------------------------------------------------------------- aba 1: UF
    with aba1:
        df_uf = uf[(uf["ano"] == ano) & (uf["sexo"] == "Total") & (uf["regiao"].isin(regioes)) & (uf["uf"].isin(ufs_sel))]
        painel(df_uf, "horas", "horas por UF")

        if len(df_uf) >= 4:
            df_uf = df_uf.sort_values("horas", ascending=False)
            st.plotly_chart(px.bar(df_uf, x="sigla", y="horas", color="regiao", title="Horas por UF"))
            st.dataframe(df_uf[["uf", "regiao", "horas"]], hide_index=True)

    # ------------------------------------------------- aba 2: homens x mulheres
    with aba2:
        df_reg = regiao[(regiao["ano"] == ano) & (regiao["regiao"].isin(regioes))]
        sexo = st.radio("Sexo", ["Mulheres", "Homens"], horizontal=True)
        painel(df_reg[df_reg["sexo"] == sexo], "horas", sexo)

        if not df_reg.empty:
            st.plotly_chart(
                px.bar(df_reg, x="regiao", y="horas", color="sexo", barmode="group",
                       facet_col="ocupacao", title="Horas por região, sexo e ocupação")
            )

    # ---------------------------------------------------- aba 3: lacuna de gênero
    with aba3:
        # Uma linha por região e ocupação, com colunas Homens e Mulheres
        larga = df_reg.pivot_table(index=["regiao", "ocupacao"], columns="sexo", values="horas")
        lacuna = larga.reset_index()
        if not lacuna.empty:
            lacuna["lacuna"] = (lacuna["Mulheres"] - lacuna["Homens"]).round(1)
        painel(lacuna, "lacuna", "lacuna Mulheres − Homens")

        if not lacuna.empty:
            st.plotly_chart(
                px.bar(lacuna, x="regiao", y="lacuna", color="ocupacao", barmode="group",
                       title="Lacuna de gênero (horas)")
            )

    # --------------------------------------------------------------- aba 4: texto
    with aba4:
        st.markdown((PASTA / "analise.md").read_text(encoding="utf-8"))
