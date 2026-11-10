# Análise descritiva — Rendimento dos Responsáveis e a Captura do Espaço Urbano

**Indicador técnico do projeto:** Transporte e Mobilidade Urbana (Censo Demográfico 2022).
**Recorte de renda disponível:** *rendimento domiciliar per capita*, não rendimento individual dos responsáveis. 
**Autor da seção:** Leonardo Barbosa Silva — Turma 3E2.

## Pergunta de negócio
Como a renda e a cor ou raça se relacionam às condições de deslocamento ao trabalho, e quais localidades merecem atenção prioritária?

## Dados, método e limites
- Fonte numérica: **IBGE, Censo Demográfico 2022**, *Deslocamentos para trabalho e para estudo — Resultados preliminares da amostra*. Os percentuais foram transcritos de quadros oficiais, identificados no código-fonte.
- Fonte de contexto: **Ipea, Projeto Acesso a Oportunidades** — estudos sobre desigualdade territorial, renda e acesso a emprego/serviços.
- A análise usa percentuais **agregados por grupos**. Sem microdados/contagens, não se calcula a mediana do tempo individual dos trabalhadores e não se faz média ponderada de regiões.
- Os valores foram publicados com uma casa decimal; podem não somar exatamente 100% pelo arredondamento.
- O título 'rendimento dos responsáveis' veio da argumentação do grupo, mas a tabela do IBGE aqui utilizada tem como categoria **renda domiciliar por morador**.
- **Não foi verificada** a afirmação de que famílias de baixa renda gastam 'até 20% da renda com transporte'; por isso não foi apresentada como um dado comprovado.

## Comparação por renda
As proporções de viagens **acima de uma hora** (soma de 61–120 minutos e mais de 120 minutos) são:

| faixa_renda    |   acima_uma_hora |
|:---------------|-----------------:|
| > 1 a 2 SM     |             12.4 |
| > 1/2 a 1 SM   |             13.4 |
| > 1/4 a 1/2 SM |             13.5 |
| > 2 a 3 SM     |             11   |
| > 3 a 5 SM     |             10   |
| > 5 SM         |              8.8 |
| Até 1/4 SM     |             11.7 |

A faixa de renda de até 1/4 do salário mínimo registra **11,7%** e a acima de cinco salários mínimos registra **8,8%**, diferença de **2,9 pontos percentuais**. O comportamento varia entre faixas e não deve ser apresentado como uma relação linear perfeita.

**Estatísticas descritivas** das 7 proporções de viagem acima de uma hora, em pontos percentuais:

- Média: **11,54**; mediana: **11,70**; moda: **não há**.
- Q1: **10,50**; Q2: **11,70**; Q3: **12,90**; IQR: **2,40**.
- Amplitude: **4,70**; variância amostral: **3,04**; desvio padrão amostral: **1,74**.
- Limites 1,5×IQR: **6,90** a **16,50**; outliers: **nenhum**.

## Comparação por cor/raça
No recorte de meio de transporte predominante durante o trajeto ao trabalho:

- **Automóvel:** pessoas brancas **42,90%** × pessoas pretas **21,00%** — diferença de **21,90 p.p.**.
- **Ônibus:** pessoas pretas **29,50%** × pessoas brancas **17,60%** — diferença de **11,90 p.p.**.

Esses percentuais não provam causalidade individual entre raça, renda e veículo. Indicam diferenças de distribuição e ajudam a formular políticas públicas para transporte coletivo e mobilidade ativa.

## Territórios de atenção
Ranking das concentrações urbanas selecionadas pelo IBGE segundo o percentual que leva **mais de uma hora**:

| cidade         |   acima_uma_hora |
|:---------------|-----------------:|
| Rio de Janeiro |             29.8 |
| São Paulo      |             27.9 |
| Manaus         |             22.9 |
| Recife         |             21.4 |
| Salvador       |             20.6 |
| Belo Horizonte |             20.4 |
| Brasília       |             20.3 |
| Belém          |             18   |

**Estatística das 15 concentrações urbanas selecionadas** (excluindo a linha de referência Brasil): média **18,12%**, mediana **18,00%**, IQR **7,95 p.p.**, desvio padrão **6,06 p.p.**; 0 outlier(s) pela regra 1,5×IQR. A amostra desta tabela **não representa todas as cidades brasileiras**.

## Recomendações à persona (secretário de Mobilidade e prefeitos)
1. Reforçar frequência e integração do transporte coletivo em corredores com deslocamento longo.
2. Medir oportunidades acessíveis em 30 e 60 minutos por transporte público, especialmente em bairros periféricos, conforme a metodologia do Ipea.
3. Integrar infraestrutura de caminhabilidade e ciclovias a oportunidades de emprego e serviços.
4. Priorizar novos levantamentos desagregados por renda e raça em nível municipal antes de adotar medidas pontuais.

## Referências
- IBGE (2025), apresentação **Deslocamentos para trabalho e para estudo — Resultados preliminares da amostra**, Censo 2022: https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/eb6833eb8d1aa7d4f77b9b38cd20fbdb.pdf
- IBGE, tabela SIDRA 10332 (transporte por nível de instrução e cor/raça): https://sidra.ibge.gov.br/tabela/10332
- Ipea, Projeto Acesso a Oportunidades: https://www.ipea.gov.br/acessooportunidades/
- Ipea, dados e metodologia: https://www.ipea.gov.br/acessooportunidades/dados/
