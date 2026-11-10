## Análise estatística: Mulheres e a "Mobilidade do Cuidado"

**Indicador.** Média de horas semanais dedicadas a afazeres domésticos e/ou cuidados de pessoas, para a população de 14 anos ou mais (IBGE, PNAD Contínua, tema *Outras formas de trabalho*, 2022). Os valores por Unidade da Federação (UF) foram conferidos no SIDRA (tabela 7015, PNAD Contínua); os valores por sexo, região e situação de ocupação vêm do Informativo *Outras formas de trabalho 2022*, do IBGE.

**O que o dado mede e o que não mede.** O IBGE não pesquisa viagens encadeadas, horários ou rotas. A PNAD mede o tempo de trabalho de cuidado não remunerado, que é a demanda que, segundo a pesquisa do IPEA citada no trabalho, gera o padrão "casa-creche-trabalho-mercado-casa". Os números abaixo sustentam a premissa de que o cuidado se concentra nas mulheres, mas não medem a mobilidade em si.

### 1. Horas de cuidado por UF (n = 27, 2022)

| Medida | Valor |
|---|---|
| Média | 16,64 h |
| Mediana (Q2) | 16,70 h |
| Moda | 13,6 h (AC, RR e AP) |
| Q1 / Q3 | 15,35 h / 17,90 h |
| IQR | 2,55 h |
| Amplitude | 6,6 h (13,6 a 20,2) |
| Variância | 3,43 h² |
| Desvio padrão | 1,85 h (coeficiente de variação de 11,1%) |

Média e mediana quase coincidem, então a distribuição é aproximadamente simétrica e a média não é distorcida por extremos. A moda (13,6 h) fica na ponta inferior porque três UFs do Norte empatam nesse valor; ela descreve esse empate, não o centro da distribuição. Pelo critério de 1,5 × IQR (faixa esperada de 11,5 a 21,7 h) não há outliers. Há, porém, um padrão regional: as três maiores médias são de UFs do Nordeste (AL 20,2; CE 19,5; PE 19,3) e a média das UFs nordestinas (18,6 h) supera a do Centro-Oeste (15,0 h) em cerca de 3,7 horas semanais.

### 2. Homens e mulheres (regiões × situação de ocupação, n = 10 por sexo)

| Medida | Homens | Mulheres |
|---|---|---|
| Média | 11,91 h | 20,52 h |
| Mediana | 11,65 h | 20,75 h |
| Moda | sem moda | sem moda |
| Q1 / Q3 | 11,03 / 12,97 | 17,65 / 22,48 |
| IQR | 1,95 h | 4,82 h |
| Amplitude | 4,1 h (9,9 a 14,0) | 9,7 h (16,2 a 25,9) |
| Variância | 1,76 h² | 12,35 h² |
| Desvio padrão | 1,33 h | 3,51 h |

No Brasil, em 2022, as mulheres dedicaram 21,3 h por semana contra 11,7 h dos homens: 9,6 horas a mais (cerca de 1,4 hora por dia), ou 1,8 vez o tempo masculino. As distribuições nem se sobrepõem: o menor valor entre os grupos de mulheres (16,2 h) é maior que o maior valor entre os grupos de homens (14,0 h). O desvio padrão feminino é 2,6 vezes o masculino, ou seja, a carga das mulheres varia muito mais conforme a região e a ocupação, enquanto a dos homens é baixa e uniforme. Em nenhum dos dois grupos há outliers.

### 3. Lacuna de gênero (mulheres menos homens, n = 10)

Média de 8,61 h, mediana de 8,9 h, distribuição bimodal (6,5 h e 9,8 h), Q1 de 6,5 h, Q3 de 9,8 h, IQR de 3,3 h, amplitude de 7,3 h (de 5,5 no Sul, entre ocupados, a 12,8 no Nordeste, entre não ocupados), variância de 5,53 h² e desvio padrão de 2,35 h. Não há outliers (faixa de 1,55 a 14,75 h). A lacuna é maior entre quem não está ocupado (média de 10,5 h) do que entre quem está (6,7 h), mas não desaparece com o emprego: no Brasil, mulheres ocupadas dedicam 17,8 h ao cuidado e homens ocupados, 11,0 h, uma diferença de 6,8 h que caracteriza a dupla jornada.

### 4. Leitura à luz das desigualdades sociais

- **Gênero.** A ausência de outliers não significa ausência de desigualdade: aqui ela aparece como deslocamento entre distribuições (mediana de 11,65 h contra 20,75 h), não como casos extremos.
- **Território.** O Nordeste concentra as maiores cargas (mulheres não ocupadas chegam a 25,9 h e mulheres ocupadas a 19,7 h, o maior valor entre as ocupadas). Fatores como menor oferta de serviços de cuidado e de infraestrutura doméstica são hipóteses plausíveis, mas estes dados não permitem testá-las.
- **Ocupação.** O trabalho remunerado não elimina o trabalho de cuidado; ele soma tempo. Esse tempo escasso é coerente com o argumento do IPEA de que as mulheres fazem trajetos curtos, múltiplos e encadeados, pagam mais tarifas de integração e escolhem horários e rotas pelo medo de assédio. Esse nexo vem da literatura citada, não foi medido aqui.

### 5. Limitações

- Os valores por UF e por região são médias de grupos estimadas por pesquisa amostral, não microdados; por isso a variância é amostral (n − 1).
- Só há recorte por UF em 2022. Para 2019 existem apenas o total do Brasil (16,8 h, contra 17,0 h em 2022) e o Espírito Santo por sexo.
- Não há tabela de UF por sexo na base usada; ela pode ser baixada do SIDRA e incluída em `dados/uf_horas_cuidado.csv` (coluna `sexo`).
- Os valores por UF foram conferidos no SIDRA (tabela 7015, variável 10192, 2022, sexo total): os 27 valores coincidem com a publicação oficial.
