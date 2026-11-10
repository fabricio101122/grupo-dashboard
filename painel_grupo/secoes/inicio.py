"""Página de abertura do painel do grupo."""
import streamlit as st


def render():
    st.title("Números que Falam: Descobrindo o Brasil")
    st.caption("Painel do grupo · Censo Demográfico 2022 (IBGE) · Python e Matemática")

    st.markdown(
        "O painel reúne os cinco indicadores do grupo. Use o **menu da barra lateral** para trocar de seção. "
        "Cada seção tem seus próprios filtros e uploads, e eles valem só para ela."
    )

    st.subheader("As cinco seções")
    st.markdown(
        "| Seção | Pergunta que a seção responde |\n"
        "|---|---|\n"
        "| 1 · Estrutura etária, sexo e raça | Em quais UFs o envelhecimento e a juventude negra pedem políticas de mobilidade diferentes? |\n"
        "| 2 · Alfabetização e deslocamento | Em quais territórios a baixa alfabetização e as viagens longas aparecem juntas? |\n"
        "| 3 · População indígena e mobilidade | Como a população indígena se divide entre áreas urbanas e rurais, e que dados faltam para avaliar a mobilidade? |\n"
        "| 4 · Mulheres e a mobilidade do cuidado | Quanto do tempo de cuidado recai sobre as mulheres, e como isso varia por região e ocupação? |\n"
        "| 5 · Rendimento e mobilidade urbana | Como renda, raça e território se associam ao tempo de deslocamento e ao meio de transporte principal? |\n"
    )

    st.subheader("Como ler os números")
    st.markdown(
        "- **Média** é sensível a valores extremos; **mediana** e **quartis** descrevem o centro sem essa distorção.\n"
        "- **IQR** (Q3 − Q1) mede a dispersão da metade central dos dados.\n"
        "- **Outliers** são valores fora de [Q1 − 1,5 × IQR; Q3 + 1,5 × IQR]. Um outlier não é erro: é um valor distante do restante.\n"
        "- Desvio padrão e variância são amostrais (divisão por n − 1)."
    )
    st.info(
        "Associações observadas nestes dados não provam causa. Os recortes são agregados, feitos por UF, região, "
        "raça ou faixa de renda, e não por pessoa."
    )
