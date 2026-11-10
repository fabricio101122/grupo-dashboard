"""Dashboard do Aluno 3 — População indígena urbana e mobilidade.
Execute com: streamlit run app.py
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from . import modulo_indigenas as mi

BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = BASE_DIR / "dados"

NOTICIAS = [
    {
        "titulo": "Censo 2022: mais da metade da população indígena vive nas cidades",
        "fonte": "Agência Gov / IBGE — 19/12/2024",
        "url": "https://agenciagov.ebc.com.br/noticias/202412/censo-2022-mais-da-metade-da-populacao-indigena-vive-nas-cidades",
        "resumo": "A divulgação apresenta 914.746 pessoas indígenas em situação urbana (53,97%) e explica que a comparação com 2010 também foi influenciada por melhorias metodológicas na captação censitária.",
    },
    {
        "titulo": "O Brasil Indígena — dados e distribuição espacial",
        "fonte": "IBGE — página temática oficial",
        "url": "https://www.ibge.gov.br/brasil-indigena/",
        "resumo": "Painel oficial com dados de população, situação do domicílio e distribuição territorial dos povos indígenas.",
    },
    {
        "titulo": "Pesquisa Nacional de Mobilidade Urbana (PEMOB) 2026",
        "fonte": "Ministério das Cidades — 28/10/2026",
        "url": "https://www.gov.br/cidades/pt-br/assuntos/mobilidade-urbana/pesquisa-nacional-de-mobilidade-urbana-pemob-2026",
        "resumo": "Disponibiliza bancos municipais e metropolitanos de mobilidade. É uma fonte complementar para investigar a oferta de transporte, mas não apresenta, por si só, recorte específico por população indígena.",
    },
]


def _imagem(coluna, arquivo, legenda):
    caminho = BASE_DIR / "assets" / arquivo
    if caminho.exists():
        coluna.image(str(caminho), caption=legenda, use_container_width=True)
    else:
        coluna.info(f"Imagem ausente: assets/{arquivo}")


def carregar_base(arquivo=None):
    caminho = arquivo if arquivo is not None else DADOS_DIR / "indigenas_ibge_2022.csv"
    bruto = mi.ler_arquivo(caminho)
    return mi.limpar_e_padronizar(bruto)


def formatar_numero(valor):
    return f"{valor:,.0f}".replace(",", ".")


def render():
    st.title("🌎 População indígena urbana e a questão da mobilidade")
    st.caption("Projeto Integrado — Números que Falam | Indicador do Aluno 3 | Fonte demográfica: IBGE, Censo 2022")
    st.markdown(
        "Este painel apresenta a distribuição da população indígena entre áreas urbanas e rurais. "
        "A mobilidade é investigada como questão social complementar: os dados demográficos não medem diretamente "
        "linhas de ônibus, tempo de viagem, calçadas ou acesso a serviços."
    )

    st.sidebar.header("📂 Base de dados")
    arquivo = st.sidebar.file_uploader("Enviar outra base do IBGE (CSV/XLSX)", type=["csv", "xlsx", "xls"])
    try:
        df = carregar_base(arquivo)
    except Exception as erro:
        st.error(f"Não foi possível carregar a base: {erro}")
        st.stop()
    if df.empty:
        st.error("A base não contém registros válidos das Unidades da Federação.")
        st.stop()

    st.sidebar.header("🎛️ Filtros disponíveis")
    regioes = sorted(df["regiao"].dropna().unique().tolist())
    regioes_sel = st.sidebar.multiselect("Região", regioes, default=regioes)
    ufs_disp = sorted(df[df["regiao"].isin(regioes_sel)]["uf"].unique().tolist())
    ufs_sel = st.sidebar.multiselect("Unidade da Federação", ufs_disp, default=ufs_disp)
    base = df[df["uf"].isin(ufs_sel)].copy()
    tab = mi.tabela_por_uf(base)
    if tab.empty:
        st.warning("Selecione ao menos uma UF para visualizar os resultados.")
        st.stop()

    urb = int(tab["Urbana"].sum())
    rur = int(tab["Rural"].sum())
    total = urb + rur
    pct_urb = urb / total * 100 if total else 0
    est_total = mi.estatisticas_descritivas(tab["Total"])
    est_pct = mi.estatisticas_descritivas(tab["pct_urbano"])
    out_total = mi.detectar_outliers(tab, "Total") if len(tab) >= 4 else tab.iloc[0:0]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("População indígena no recorte", formatar_numero(total))
    k2.metric("Em situação urbana", f"{pct_urb:.2f}%", formatar_numero(urb) + " pessoas")
    k3.metric("Em situação rural", formatar_numero(rur))
    k4.metric("Mediana por UF", formatar_numero(est_total["mediana"]))

    t1, t2, t3, t4, t5 = st.tabs(["📍 Panorama", "🧮 Estatística", "📈 Evolução", "🚌 Mobilidade e notícias", "🗃️ Dados"])

    with t1:
        st.subheader("Distribuição da população indígena por UF")
        longa = tab.melt(id_vars=["uf", "sigla", "regiao"], value_vars=["Urbana", "Rural"],
                         var_name="Situação do domicílio", value_name="Pessoas")
        ordem = tab.sort_values("Total", ascending=False)["sigla"].tolist()
        fig = px.bar(longa, x="sigla", y="Pessoas", color="Situação do domicílio", barmode="stack",
                     category_orders={"sigla": ordem}, hover_data=["uf"],
                     title="População indígena em situação urbana e rural por UF",
                     color_discrete_map={"Urbana": "#2563eb", "Rural": "#16a34a"})
        st.plotly_chart(fig, use_container_width=True)
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.pie(values=[urb, rur], names=["Urbana", "Rural"], hole=.55,
                               title="Participação urbana e rural no recorte",
                               color_discrete_sequence=["#2563eb", "#16a34a"]), use_container_width=True)
        c2.plotly_chart(px.bar(tab.sort_values("pct_urbano"), x="pct_urbano", y="uf", orientation="h",
                               title="Percentual urbano por UF", labels={"pct_urbano": "% urbano", "uf": "UF"}),
                        use_container_width=True)
        mapa = tab.copy()
        mapa["lat"] = mapa["sigla"].map(lambda s: mi.CENTROIDE_UF[s][0])
        mapa["lon"] = mapa["sigla"].map(lambda s: mi.CENTROIDE_UF[s][1])
        mapa_fig = px.scatter_geo(mapa, lat="lat", lon="lon", size="Total", color="pct_urbano",
                                  hover_name="uf", hover_data={"Urbana": True, "Rural": True,
                                  "lat": False, "lon": False, "pct_urbano": ":.1f"},
                                  title="Distribuição por UF — tamanho: população total; cor: percentual urbano",
                                  color_continuous_scale="Viridis", size_max=42)
        mapa_fig.update_geos(scope="south america", fitbounds="locations", showcountries=True,
                             showland=True, landcolor="#f1f5f9")
        st.plotly_chart(mapa_fig, use_container_width=True)
        st.caption("O mapa utiliza centroides aproximados das UFs; não representa a localização de comunidades ou territórios indígenas.")

    with t2:
        escolha = st.radio("Variável", ["População total por UF", "Percentual urbano por UF"], horizontal=True)
        coluna = "Total" if escolha.startswith("População") else "pct_urbano"
        est = est_total if coluna == "Total" else est_pct
        unidade = " pessoas" if coluna == "Total" else " p.p."
        fmt = formatar_numero if coluna == "Total" else lambda x: f"{x:.2f}"
        a, b, c, d = st.columns(4)
        a.metric("Média", fmt(est["media"]) + unidade)
        b.metric("Mediana", fmt(est["mediana"]) + unidade)
        c.metric("Moda", fmt(est["moda"]) if est["tem_moda"] else "Sem moda")
        d.metric("Desvio padrão", fmt(est["desvio_padrao"]) + unidade)
        e, f, g, h = st.columns(4)
        e.metric("Q1", fmt(est["q1"]) + unidade)
        f.metric("Q3", fmt(est["q3"]) + unidade)
        g.metric("IQR", fmt(est["iqr"]) + unidade)
        h.metric("Amplitude", fmt(est["amplitude"]) + unidade)
        st.caption(f"Variância: {est['variancia']:.3f} | Coeficiente de variação: {est['coef_variacao']:.2f}% | n = {est['n']} UFs | Desvio padrão amostral (ddof=1).")
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.box(tab, y=coluna, points="all", hover_name="uf", title="Boxplot"), use_container_width=True)
        c2.plotly_chart(px.histogram(tab, x=coluna, nbins=10, title="Histograma"), use_container_width=True)
        out = mi.detectar_outliers(tab, coluna) if len(tab) >= 4 else tab.iloc[0:0]
        st.subheader("Valores extremos — regra de 1,5 × IQR")
        if out.empty:
            st.success("Nenhuma UF identificada como outlier neste recorte.")
        else:
            st.dataframe(out, use_container_width=True)
        st.caption("Outlier estatístico não significa erro: indica um valor distante do restante da distribuição.")

    with t3:
        st.subheader("Evolução nacional — 2010 e 2022")
        caminho_evolucao = DADOS_DIR / "evolucao_nacional_2010_2022.csv"
        if not caminho_evolucao.exists():
            st.info("Falta o arquivo dados/evolucao_nacional_2010_2022.csv. Coloque-o na pasta dados/ para ver esta aba.")
        else:
            evolucao = pd.read_csv(DADOS_DIR / "evolucao_nacional_2010_2022.csv")
            longa_evolucao = evolucao.melt(id_vars="ano", value_vars=["urbana", "rural"],
                                           var_name="Situação", value_name="Pessoas")
            st.plotly_chart(px.bar(longa_evolucao, x="ano", y="Pessoas", color="Situação", barmode="group",
                                   text_auto=".3s", title="População indígena por situação do domicílio"),
                            use_container_width=True)
            st.dataframe(evolucao.rename(columns={"ano": "Ano", "urbana": "Urbana", "rural": "Rural", "total": "Total"}),
                         hide_index=True, use_container_width=True)
            st.info("A comparação entre 2010 e 2022 exige cautela: o IBGE informa que aperfeiçoamentos metodológicos e de captação também influenciaram a variação. Esta série é nacional; não permite comparar a evolução de cada UF.")

    with t4:
        st.subheader("O que sabemos sobre mobilidade — e o que ainda precisa ser medido")
        st.markdown(
            "O Censo mostra a presença indígena nas cidades, mas não mede a qualidade do transporte. "
            "Para avaliar exclusão de mobilidade, é necessário cruzar a localização das comunidades com "
            "linhas e horários de ônibus, tarifa, tempo de viagem, acessibilidade de calçadas e distância "
            "até escolas, unidades de saúde e locais de trabalho."
        )
        st.warning("Não há uma base real de viagens indígenas anexada a este projeto. Não apresentamos medianas de deslocamento ou comparação racial sem observações verificáveis.")
        st.markdown("**Fonte complementar recomendada:** a PEMOB 2026, do Ministério das Cidades, reúne informações municipais e metropolitanas sobre mobilidade. Ela ajuda a estudar a oferta geral de transporte, mas não deve ser tratada como dado específico da população indígena.")
        st.link_button("Consultar dados da PEMOB 2026", NOTICIAS[2]["url"])
        st.divider()
        st.subheader("Visualizações de apoio")
        img1, img2 = st.columns(2)
        _imagem(img1, "distribuicao_nacional.png", "Distribuição nacional urbana/rural — IBGE, 2022")
        _imagem(img2, "percentual_urbano_ufs.png", "Percentual urbano por UF — cálculo a partir da base do IBGE, 2022")
        st.subheader("Notícias e fontes para contextualização")
        for noticia in NOTICIAS:
            with st.container(border=True):
                st.markdown(f"**{noticia['titulo']}**")
                st.caption(noticia["fonte"])
                st.write(noticia["resumo"])
                st.markdown(f"[Abrir fonte]({noticia['url']})")
        st.divider()
        st.subheader("Base complementar própria — opcional")
        st.caption("Se o grupo conseguir uma pesquisa real de deslocamento, envie CSV/XLSX com as colunas: cor_raca, meio_transporte e tempo_min. Não use dados simulados como se fossem reais.")
        arquivo_mob = st.file_uploader("Enviar pesquisa de mobilidade", type=["csv", "xlsx", "xls"], key="mobilidade")
        if arquivo_mob is not None:
            try:
                mob = mi.padronizar_mobilidade(mi.ler_arquivo(arquivo_mob))
                mob["grupo_modal"] = mob["meio_transporte"].map(mi.agrupar_modal)
                medianas = mob.groupby("cor_raca")["tempo_min"].median().sort_values(ascending=False)
                st.metric("Maior mediana observada (minutos)", f"{medianas.iloc[0]:.1f}", str(medianas.index[0]))
                st.plotly_chart(px.box(mob, x="cor_raca", y="tempo_min", color="grupo_modal",
                                       title="Tempo de deslocamento por grupo informado e modal"), use_container_width=True)
                st.caption("Resultados válidos somente para a amostra enviada; informe tamanho, local, período e método de coleta antes de interpretar.")
            except Exception as erro:
                st.error(f"Não foi possível processar a base complementar: {erro}")

    with t5:
        st.subheader("Dados utilizados")
        st.dataframe(tab[["uf", "sigla", "regiao", "Urbana", "Rural", "Total", "pct_urbano"]],
                     hide_index=True, use_container_width=True)
        csv = tab.to_csv(index=False).encode("utf-8-sig")
        st.download_button("Baixar recorte filtrado em CSV", data=csv,
                           file_name="populacao_indigena_recorte.csv", mime="text/csv")
        st.markdown("**Dicionário:** Urbana e Rural são contagens absolutas; Total é a soma; pct_urbano é Urbana ÷ Total × 100.")
        st.markdown("**Fonte:** IBGE, Censo Demográfico 2022, Tabela 9. Consulte `dados/FONTE_DOS_DADOS.md`.")

    st.divider()
    st.caption("Projeto acadêmico. Os resultados dependem do recorte selecionado e das limitações descritas nas fontes.")
