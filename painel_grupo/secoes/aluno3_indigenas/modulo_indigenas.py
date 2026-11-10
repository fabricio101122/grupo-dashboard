"""
Módulo do Aluno 3 – População Indígena (urbano x rural) e exclusão da mobilidade.

Contém SOMENTE lógica (ETL + estatística), sem Streamlit, para poder ser
testada e reaproveitada pelo painel unificado do grupo.
"""
from __future__ import annotations

import unicodedata
from typing import Optional

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Constantes
# ----------------------------------------------------------------------------
REGIAO_POR_UF = {
    "Rondônia": "Norte", "Acre": "Norte", "Amazonas": "Norte", "Roraima": "Norte",
    "Pará": "Norte", "Amapá": "Norte", "Tocantins": "Norte",
    "Maranhão": "Nordeste", "Piauí": "Nordeste", "Ceará": "Nordeste",
    "Rio Grande do Norte": "Nordeste", "Paraíba": "Nordeste", "Pernambuco": "Nordeste",
    "Alagoas": "Nordeste", "Sergipe": "Nordeste", "Bahia": "Nordeste",
    "Minas Gerais": "Sudeste", "Espírito Santo": "Sudeste",
    "Rio de Janeiro": "Sudeste", "São Paulo": "Sudeste",
    "Paraná": "Sul", "Santa Catarina": "Sul", "Rio Grande do Sul": "Sul",
    "Mato Grosso do Sul": "Centro-Oeste", "Mato Grosso": "Centro-Oeste",
    "Goiás": "Centro-Oeste", "Distrito Federal": "Centro-Oeste",
}
SIGLA_POR_UF = {
    "Rondônia": "RO", "Acre": "AC", "Amazonas": "AM", "Roraima": "RR", "Pará": "PA",
    "Amapá": "AP", "Tocantins": "TO", "Maranhão": "MA", "Piauí": "PI", "Ceará": "CE",
    "Rio Grande do Norte": "RN", "Paraíba": "PB", "Pernambuco": "PE", "Alagoas": "AL",
    "Sergipe": "SE", "Bahia": "BA", "Minas Gerais": "MG", "Espírito Santo": "ES",
    "Rio de Janeiro": "RJ", "São Paulo": "SP", "Paraná": "PR", "Santa Catarina": "SC",
    "Rio Grande do Sul": "RS", "Mato Grosso do Sul": "MS", "Mato Grosso": "MT",
    "Goiás": "GO", "Distrito Federal": "DF",
}
# Centroides APROXIMADOS (lat, lon) para o mapa de bolhas por UF
CENTROIDE_UF = {
    "RO": (-10.83, -63.34), "AC": (-9.02, -70.81), "AM": (-3.47, -65.10), "RR": (2.00, -61.40),
    "PA": (-3.79, -52.48), "AP": (1.41, -51.77), "TO": (-10.18, -48.33), "MA": (-5.42, -45.44),
    "PI": (-7.72, -42.73), "CE": (-5.20, -39.53), "RN": (-5.81, -36.59), "PB": (-7.12, -36.72),
    "PE": (-8.38, -37.86), "AL": (-9.62, -36.82), "SE": (-10.57, -37.45), "BA": (-12.96, -41.70),
    "MG": (-18.51, -44.55), "ES": (-19.19, -40.34), "RJ": (-22.25, -42.66), "SP": (-22.19, -48.79),
    "PR": (-24.89, -51.55), "SC": (-27.45, -50.95), "RS": (-30.17, -53.50), "MS": (-20.51, -54.54),
    "MT": (-12.64, -55.42), "GO": (-15.98, -49.86), "DF": (-15.78, -47.93),
}


def _sem_acento(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", str(txt))
    return "".join(c for c in txt if not unicodedata.combining(c)).lower().strip()


# ----------------------------------------------------------------------------
# ETL
# ----------------------------------------------------------------------------
def ler_arquivo(arquivo) -> pd.DataFrame:
    """Lê CSV ou XLSX (caminho ou objeto do st.file_uploader)."""
    nome = getattr(arquivo, "name", str(arquivo)).lower()
    if nome.endswith((".xlsx", ".xls")):
        return pd.read_excel(arquivo, dtype=str)
    # CSV: tenta ; e , e codificações comuns do IBGE
    for enc in ("utf-8-sig", "latin-1"):
        for sep in (";", ","):
            try:
                if hasattr(arquivo, "seek"):
                    arquivo.seek(0)
                df = pd.read_csv(arquivo, sep=sep, encoding=enc, dtype=str)
                if df.shape[1] > 1:
                    return df
            except Exception:
                continue
    raise ValueError("Não foi possível ler o arquivo. Use CSV (; ou ,) ou XLSX.")


def _achar_coluna(df: pd.DataFrame, *palavras: str) -> Optional[str]:
    # ignora colunas de código do SIDRA, ex.: "Unidade da Federação (Código)"
    for col in df.columns:
        c = _sem_acento(col)
        if "(codigo)" in c:
            continue
        if any(p in c for p in palavras):
            return col
    return None


def limpar_e_padronizar(bruto: pd.DataFrame) -> pd.DataFrame:
    """
    Converte uma tabela do SIDRA/IBGE (ou já tratada) para o esquema padrão:
        uf | regiao | ano | situacao (Urbana/Rural) | sexo | pop_indigena
    Passos: cabeçalho SIDRA -> nomes de coluna -> tipos -> nulos -> totais -> região.
    """
    df = bruto.copy()

    # SIDRA costuma trazer a 1ª linha como cabeçalho real (ex.: "Valor", "Unidade...")
    primeira = [_sem_acento(v) for v in df.iloc[0].tolist()] if len(df) else []
    if "valor" in primeira:
        df.columns = df.iloc[0].tolist()
        df = df.iloc[1:].reset_index(drop=True)

    c_uf = _achar_coluna(df, "unidade da federacao", "uf", "estado")
    c_val = _achar_coluna(df, "pop_indigena", "valor", "populacao", "pessoas")
    c_sit = _achar_coluna(df, "situacao", "domicilio")
    c_sex = _achar_coluna(df, "sexo")
    c_ano = _achar_coluna(df, "ano")
    c_idade = _achar_coluna(df, "grupo de idade", "grupos de idade", "faixa")  # "idade" solto casaria com "unidade"
    if c_idade is None:
        c_idade = next((c for c in df.columns if _sem_acento(c) in ("idade", "faixa_etaria")), None)
    c_cor = _achar_coluna(df, "cor ou raca", "cor_raca")
    if c_cor:  # tabelas do SIDRA trazem várias cores/raças: ficamos só com indígenas
        df = df[df[c_cor].map(_sem_acento).str.contains("indigen")]
    if c_uf is None or c_val is None:
        raise ValueError(
            "Não encontrei colunas de UF e de valor. Colunas lidas: "
            f"{list(df.columns)}"
        )

    out = pd.DataFrame({"uf": df[c_uf].astype(str).str.strip()})
    out["ano"] = pd.to_numeric(df[c_ano], errors="coerce") if c_ano else 2022
    out["ano"] = out["ano"].fillna(2022).astype(int)
    out["situacao"] = df[c_sit].astype(str).str.strip() if c_sit else "Total"
    out["sexo"] = df[c_sex].astype(str).str.strip() if c_sex else "Total"
    out["faixa_etaria"] = df[c_idade].astype(str).str.strip() if c_idade else "Total"

    # valores do IBGE: "-", "X", "..." = sem dado/sigilo; milhar com ponto, decimal com vírgula
    val = df[c_val].astype(str).str.strip()
    val = val.replace({"-": np.nan, "X": np.nan, "..": np.nan, "...": np.nan, "": np.nan})
    val = val.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    out["pop_indigena"] = pd.to_numeric(val, errors="coerce")

    # padroniza rótulos de situação
    def _sit(x: str) -> str:
        x = _sem_acento(x)
        if "urban" in x:
            return "Urbana"
        if "rural" in x:
            return "Rural"
        return "Total"

    out["situacao"] = out["situacao"].map(_sit)
    out["sexo"] = out["sexo"].replace({"Homens": "Homens", "Mulheres": "Mulheres"})

    # remove Brasil/Regiões e linhas sem dado; mantém só as 27 UFs
    out = out[out["uf"].isin(REGIAO_POR_UF)].dropna(subset=["pop_indigena"])
    out["regiao"] = out["uf"].map(REGIAO_POR_UF)
    out["sigla"] = out["uf"].map(SIGLA_POR_UF)
    out = out.drop_duplicates()
    return out[["uf", "sigla", "regiao", "ano", "situacao", "sexo", "faixa_etaria",
                "pop_indigena"]].reset_index(drop=True)


def filtrar_dimensao(df: pd.DataFrame, coluna: str, valor: str) -> pd.DataFrame:
    """Filtra sexo/faixa etária sem dupla contagem. 'Todos' usa a linha 'Total' se existir; senão soma tudo."""
    if valor == "Todos":
        return df[df[coluna] == "Total"] if (df[coluna] == "Total").any() else df
    return df[df[coluna] == valor]


def serie_temporal(df: pd.DataFrame) -> pd.DataFrame:
    """Urbana, rural, total e % urbano por ano (df já filtrado por UF/sexo/faixa)."""
    base = df[df["situacao"].isin(["Urbana", "Rural"])]
    piv = base.pivot_table(index="ano", columns="situacao", values="pop_indigena",
                           aggfunc="sum", fill_value=0).reset_index()
    for c in ("Urbana", "Rural"):
        if c not in piv:
            piv[c] = 0
    piv["Total"] = piv["Urbana"] + piv["Rural"]
    piv["pct_urbano"] = np.where(piv["Total"] > 0, piv["Urbana"] / piv["Total"] * 100, np.nan)
    return piv


def tabela_por_uf(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por UF: urbana, rural, total e % urbano (usa linhas Urbana/Rural)."""
    base = df[df["situacao"].isin(["Urbana", "Rural"])]
    # o chamador deve ter filtrado sexo e faixa etária (veja filtrar_dimensao) para evitar dupla contagem
    piv = base.pivot_table(index=["uf", "sigla", "regiao"], columns="situacao",
                           values="pop_indigena", aggfunc="sum", fill_value=0).reset_index()
    for c in ("Urbana", "Rural"):
        if c not in piv:
            piv[c] = 0
    piv["Total"] = piv["Urbana"] + piv["Rural"]
    piv["pct_urbano"] = np.where(piv["Total"] > 0, piv["Urbana"] / piv["Total"] * 100, np.nan)
    return piv.sort_values("Total", ascending=False).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Estatística (todas as métricas exigidas no enunciado)
# ----------------------------------------------------------------------------
def estatisticas_descritivas(serie: pd.Series) -> dict:
    """Média, mediana, moda, Q1/Q2/Q3, IQR, amplitude, variância, desvio, CV e outliers (1,5×IQR)."""
    s = pd.to_numeric(serie, errors="coerce").dropna()
    if s.empty:
        raise ValueError("Série vazia.")
    q1, q2, q3 = s.quantile([0.25, 0.5, 0.75])
    iqr = q3 - q1
    lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    frequencias = s.round(1).value_counts()
    frequencia_maxima = int(frequencias.max())
    moda = frequencias[frequencias == frequencia_maxima].index.tolist() if frequencia_maxima > 1 else []
    media = s.mean()
    # Convenção do grupo: desvio amostral (ddof=1), pois os dados são de pesquisa amostral.
    desvio = s.std(ddof=1) if len(s) > 1 else 0.0
    return {
        "n": int(len(s)),
        "media": media,
        "mediana": q2,
        "moda": float(moda[0]) if moda else np.nan,
        "moda_unica": bool(len(moda) == 1),
        "tem_moda": bool(moda),
        "q1": q1, "q2": q2, "q3": q3, "iqr": iqr,
        "minimo": s.min(), "maximo": s.max(), "amplitude": s.max() - s.min(),
        "variancia": s.var(ddof=1) if len(s) > 1 else 0.0,
        "desvio_padrao": desvio,
        "coef_variacao": (desvio / media * 100) if media else np.nan,
        "assimetria": s.skew() if len(s) > 2 else np.nan,
        "limite_inferior": lim_inf, "limite_superior": lim_sup,
    }


def detectar_outliers(tab: pd.DataFrame, coluna: str) -> pd.DataFrame:
    """Retorna as UFs fora de [Q1-1,5·IQR ; Q3+1,5·IQR] para a coluna informada."""
    est = estatisticas_descritivas(tab[coluna])
    mask = (tab[coluna] < est["limite_inferior"]) | (tab[coluna] > est["limite_superior"])
    out = tab.loc[mask, ["uf", "sigla", "regiao", coluna]].copy()
    out["tipo"] = np.where(out[coluna] > est["limite_superior"], "alto", "baixo")
    return out.sort_values(coluna, ascending=False)


def texto_analitico(tab: pd.DataFrame, est_total: dict, est_pct: dict, outl_total: pd.DataFrame) -> str:
    """Gera um texto interpretativo a partir dos números (base para a análise descritiva)."""
    urb, rur = tab["Urbana"].sum(), tab["Rural"].sum()
    pct_br = urb / (urb + rur) * 100 if (urb + rur) else np.nan
    top = tab.iloc[0]
    menos_urb = tab.loc[tab["pct_urbano"].idxmin()]
    mais_urb = tab.loc[tab["pct_urbano"].idxmax()]
    fmt = lambda x: f"{x:,.0f}".replace(",", ".")
    linhas = [
        f"Nas UFs selecionadas, {pct_br:.1f}% da população indígena vive em área urbana "
        f"({fmt(urb)} urbana x {fmt(rur)} rural).",
        f"A média de indígenas por UF ({fmt(est_total['media'])}) é "
        f"{'maior' if est_total['media'] > est_total['mediana'] else 'menor'} que a mediana "
        f"({fmt(est_total['mediana'])}): "
        + ("a distribuição é assimétrica à direita; poucas UFs concentram a população e puxam a média para cima."
           if est_total["media"] > est_total["mediana"] else "não há puxada relevante da média por valores altos."),
        f"{top['uf']} é a UF com mais indígenas ({fmt(top['Total'])}).",
        f"O % urbano varia de {menos_urb['pct_urbano']:.1f}% ({menos_urb['uf']}) a "
        f"{mais_urb['pct_urbano']:.1f}% ({mais_urb['uf']}) — amplitude de {est_pct['amplitude']:.1f} p.p., "
        f"desvio padrão de {est_pct['desvio_padrao']:.1f} p.p.",
    ]
    if not outl_total.empty:
        nomes = ", ".join(outl_total["uf"].tolist())
        linhas.append(f"Pela regra 1,5×IQR, são outliers em volume absoluto: {nomes}. "
                      "Eles distorcem a média e por isso a mediana é a medida mais representativa.")
    else:
        linhas.append("Pela regra 1,5×IQR não há outliers em volume absoluto neste recorte.")
    return "\n\n".join(linhas)


# ----------------------------------------------------------------------------
# Módulo opcional de mobilidade (tempo de deslocamento por raça/modal)
# ----------------------------------------------------------------------------
COLUNAS_MOBILIDADE = ["uf", "cor_raca", "meio_transporte", "tempo_min"]


def padronizar_mobilidade(bruto: pd.DataFrame) -> pd.DataFrame:
    df = bruto.copy()
    ren = {}
    for alvo, chaves in {
        "uf": ("uf", "unidade da federacao", "estado"),
        "cor_raca": ("cor", "raca"),
        "meio_transporte": ("meio", "modal", "transporte"),
        "tempo_min": ("tempo", "minutos", "valor"),
    }.items():
        c = _achar_coluna(df, *chaves)
        if c is None:
            raise ValueError(f"Coluna '{alvo}' não encontrada. Colunas: {list(df.columns)}")
        ren[c] = alvo
    df = df.rename(columns=ren)[COLUNAS_MOBILIDADE]
    df["tempo_min"] = pd.to_numeric(df["tempo_min"].astype(str).str.replace(",", "."), errors="coerce")
    return df.dropna(subset=["tempo_min"]).reset_index(drop=True)


def agrupar_modal(meio: str) -> str:
    m = _sem_acento(meio)
    if any(k in m for k in ("onibus", "metro", "trem", "brt", "van", "coletivo", "publico")):
        return "Público"
    if any(k in m for k in ("carro", "moto", "automovel", "particular", "taxi", "aplicativo")):
        return "Particular"
    if any(k in m for k in ("pe", "bicic", "ativo", "caminh")):
        return "Ativo"
    return "Outro"
