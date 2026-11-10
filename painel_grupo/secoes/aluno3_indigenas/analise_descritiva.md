# Análise descritiva — População indígena urbana e a questão da mobilidade
**Projeto Integrado “Números que Falam” — Aluno 3**

## 1. Pergunta de investigação
Como a população indígena se distribui entre áreas urbanas e rurais nas Unidades da Federação? Essa distribuição ajuda a identificar onde é necessário investigar se a mobilidade urbana conecta adequadamente as comunidades indígenas aos serviços de saúde, educação e trabalho?

## 2. Fonte e tratamento
- **Fonte principal:** IBGE, Censo Demográfico 2022, publicação *Indígenas: Principais características das pessoas e dos domicílios, por situação urbana ou rural do domicílio*, Tabela 9, páginas impressas 137–138.
- **Recorte:** Brasil, 27 UFs, situação urbana e rural.
- **Tratamento:** padronização dos nomes de UFs, siglas e regiões; conversão dos valores para números inteiros; organização em duas linhas por UF (Urbana e Rural); conferência da soma Urbana + Rural.
- **Tamanho da base:** 54 registros (27 UFs × 2 situações).

## 3. Panorama nacional
O Censo 2022 contabilizou **1.694.836 pessoas indígenas** no Brasil. Desse total, **914.746 (53,97%)** estavam em situação urbana e **780.090 (46,03%)** em situação rural. Portanto, mais da metade da população indígena residia em áreas urbanas.

Em 2010, o IBGE registrou 324.834 pessoas indígenas em situação urbana; em 2022, foram 914.746. O IBGE calcula aumento de 181,6%, mas ressalta que a variação não pode ser explicada exclusivamente por migração ou crescimento demográfico: aperfeiçoamentos metodológicos e melhor captação da população indígena também influenciaram a comparação.

## 4. Estatística descritiva — total de indígenas por UF
Variável: população total (urbana + rural) em cada UF, n = 27.

| Medida | Resultado |
|---|---:|
| Média | 62.771,70 pessoas |
| Mediana (Q2) | 30.466 pessoas |
| Moda | Não há moda (valores sem repetição) |
| Q1 | 18.255,50 |
| Q3 | 57.761 |
| IQR | 39.505,50 |
| Mínimo | 4.710 (Sergipe) |
| Máximo | 490.935 (Amazonas) |
| Amplitude | 486.225 pessoas |
| Desvio padrão amostral | 98.047,81 pessoas |
| Coeficiente de variação | 153,28% |

**Interpretação:** a média é muito maior que a mediana. Isso indica assimetria à direita: algumas UFs com contingentes elevados aumentam a média. A mediana representa melhor o centro da distribuição. O coeficiente de variação elevado mostra grande heterogeneidade no volume de população indígena entre as UFs.

### Outliers — regra de 1,5 × IQR
- Limite inferior: −41.002,75.
- Limite superior: 117.019,25.
- Outliers superiores: **Amazonas (490.935)** e **Bahia (229.443)**.

Esses valores são extremos em relação à distribuição das 27 UFs. Não são erros: representam concentrações reais de população indígena nesses estados.

## 5. Percentual urbano por UF
Variável: população urbana ÷ população total da UF × 100.

| Medida | Resultado |
|---|---:|
| Média simples dos percentuais estaduais | 52,15% |
| Mediana | 51,67% |
| Moda | Não há moda |
| Q1 | 33,62% |
| Q3 | 61,70% |
| IQR | 28,08 pontos percentuais |
| Mínimo | 17,34% (Mato Grosso) |
| Máximo | 95,52% (Goiás) |
| Amplitude | 78,19 pontos percentuais |
| Desvio padrão amostral | 24,13 pontos percentuais |
| Coeficiente de variação | 45,41% |
| Outliers por 1,5 × IQR | Nenhum |

**Interpretação:** há grande variação entre as UFs. Goiás (95,52%), Rio de Janeiro (94,59%) e Distrito Federal (91,84%) apresentam os maiores percentuais urbanos. Mato Grosso (17,34%), Maranhão (20,46%) e Tocantins (20,95%) apresentam os menores.

**Cuidado estatístico:** a média simples dos percentuais estaduais (52,15%) não corresponde ao percentual nacional (53,97%). A média simples atribui o mesmo peso a cada UF; o percentual nacional considera o número de pessoas de cada UF.

## 6. Contexto de infraestrutura urbana — dado complementar
Na página temática *O Brasil Indígena*, o IBGE apresenta um indicador de precariedade em pelo menos um dos serviços de abastecimento de água, esgotamento sanitário ou destinação do lixo. O quadro divulgado registra **44,30% para indígenas em áreas urbanas fora de Terras Indígenas**, enquanto o percentual da população urbana total é **18,71%**.

Esse dado sugere desigualdades relevantes de infraestrutura e serviços urbanos. Porém, ele **não mede transporte público nem mobilidade**. É um indicador contextual de condições urbanas, não uma prova de falta de ônibus, calçadas ou ciclovias. Para definição, universo e denominadores, consultar diretamente o IBGE.

## 7. O que os dados dizem — e o que ainda não dizem — sobre mobilidade
Os dados demonstram que a presença indígena urbana é expressiva e varia muito entre as UFs. Isso reforça a necessidade de políticas urbanas que considerem as comunidades indígenas como parte da população das cidades.

Entretanto, a base censitária usada no painel não informa frequência de ônibus, tempo de viagem, preço de tarifa, distância até unidades de saúde ou locais de trabalho, existência de calçadas ou ciclovias. Portanto, não é correto afirmar, com base apenas nessa tabela, que determinada comunidade sofre desconexão de transporte. A exclusão da mobilidade é uma **hipótese de investigação** que precisa ser testada com dados específicos de transporte e escuta das próprias comunidades.

A Pesquisa Nacional de Mobilidade Urbana (PEMOB) 2026, do Ministério das Cidades, disponibiliza informações municipais e metropolitanas sobre mobilidade. Pode ajudar a caracterizar a oferta geral de transporte, mas seus dados agregados não identificam automaticamente a população indígena. O cruzamento territorial precisa ser feito com cuidado e não permite atribuir diferenças étnicas sem uma variável específica e confiável.

## 8. Recomendações para a gestão pública
1. Mapear, em escala municipal e de bairro, a localização das comunidades indígenas urbanas, respeitando privacidade, segurança e participação comunitária.
2. Cruzar esses territórios com linhas, frequência e horários do transporte coletivo e com a localização de unidades de saúde, escolas e oportunidades de trabalho.
3. Medir tempos e custos reais de deslocamento, considerando diferentes modais e horários.
4. Avaliar calçadas, travessias, acessibilidade e infraestrutura cicloviária nos trajetos relevantes.
5. Construir prioridades com participação de organizações e lideranças indígenas, sem tratar povos distintos como um grupo homogêneo.

## 9. Resposta à pergunta de investigação
O Censo mostra que **914.746 pessoas indígenas viviam em situação urbana em 2022 (53,97%)** e que há UFs com percentuais urbanos muito elevados. A gestão pública deve identificar onde essas pessoas vivem nos municípios e medir a conexão efetiva com serviços essenciais. O planejamento deve combinar dados territoriais, indicadores de transporte e participação comunitária.

## 10. Limitações
- O recorte por UF esconde desigualdades entre municípios e bairros.
- Situação urbana/rural não equivale a acesso ou qualidade de transporte.
- O Censo é de 2022; redes de transporte podem ter mudado depois da coleta.
- A comparação 2010–2022 exige cautela devido aos aperfeiçoamentos metodológicos apontados pelo IBGE.
- A PEMOB é uma fonte agregada de mobilidade; não é, por si só, um levantamento de viagens da população indígena.
- Os dados não substituem pesquisa de campo nem consulta às comunidades.

## 11. Referências
- IBGE. *Censo Demográfico 2022: Indígenas — Principais características das pessoas e dos domicílios, por situação urbana ou rural do domicílio*. Tabela 9, p. 137–138. https://www.ibge.gov.br/biblioteca/visualizacao/livros/liv102155.pdf
- IBGE. *O Brasil Indígena*. https://www.ibge.gov.br/brasil-indigena/
- Agência Gov / IBGE. “Censo 2022: mais da metade da população indígena vive nas cidades”, 19 dez. 2024. https://agenciagov.ebc.com.br/noticias/202412/censo-2022-mais-da-metade-da-populacao-indigena-vive-nas-cidades
- Ministério das Cidades. *Pesquisa Nacional de Mobilidade Urbana — PEMOB 2026*, 28 out. 2026. https://www.gov.br/cidades/pt-br/assuntos/mobilidade-urbana/pesquisa-nacional-de-mobilidade-urbana-pemob-2026
