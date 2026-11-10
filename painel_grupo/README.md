# Números que Falam: painel unificado do grupo

Um único app Streamlit com as cinco seções individuais, navegação pela barra lateral e uma página de abertura.

## Como rodar

Dentro da pasta `painel_grupo`:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Se `python` não funcionar no Windows, use `py` no lugar.

## Estrutura

```
painel_grupo/
├── app.py                      # único set_page_config; menu da barra lateral; chama a seção escolhida
├── requirements.txt            # união das dependências dos cinco projetos
├── .streamlit/config.toml      # tema
└── secoes/
    ├── inicio.py               # página de abertura
    ├── aluno1_estrutura_etaria/   pagina.py (render) + modulo.py (ETL e estatísticas)
    ├── aluno2_alfabetizacao/      pagina.py (render) + analise.py + dados/ + assets/
    ├── aluno3_indigenas/          pagina.py (render) + modulo_indigenas.py + dados/
    ├── aluno4_mulheres_cuidado/   pagina.py (render) + dados/ + analise.md
    └── aluno5_renda_mobilidade/   modulos/renda_mobilidade.py (renderizar_indicador) + src/ + dados/ + assets/
```

Cada seção é uma pasta independente. O `app.py` só importa a seção quando ela é escolhida, então um erro numa seção não derruba as outras.

## Situação de cada seção

| Seção | Dados | O que falta |
|---|---|---|
| 1 · Estrutura etária | Incluído (SIDRA 9606, `dados/populacao_9606_uf_sexo_raca_idade_2022.csv`); somas por raça e razão de sexo conferidas com o IBGE | Nada. |
| 2 · Alfabetização e deslocamento | Incluídos (SIDRA 9543 e 10333, baixados da API do IBGE) | Nada. |
| 3 · População indígena | Dados incluídos (`indigenas_ibge_2022.csv` e `evolucao_nacional_2010_2022.csv`, SIDRA/IBGE) | Nada. |
| 4 · Mulheres e cuidado | Incluídos; valores por UF conferidos no SIDRA (tabela 7015): 27 de 27 iguais | Nada. |
| 5 · Rendimento e mobilidade | Incluídos (tabelas transcritas de gráficos oficiais do IBGE) | Nada. |

## Decisões para o grupo antes de entregar

1. **Desvio padrão e variância: decidido.** Todas as seções usam a convenção **amostral** (`ddof=1`). As seções 3 e 5 foram ajustadas, e os números dos documentos de análise foram recalculados.
2. **Nomes dos integrantes.** Preencher a identificação dos cinco integrantes e o indicador de cada um no relatório do grupo (a tabela da seção de integrantes).
3. **Relatório ou slides (1–2 páginas)** do grupo: ainda não foram feitos.

## Alterações feitas em relação aos projetos individuais

Nenhuma fórmula estatística foi alterada. As mudanças são de integração:

- Todas as páginas viraram uma função `render()` (a seção 5 já tinha `renderizar_indicador()`).
- `st.set_page_config` foi removido de todas as seções; ele fica só no `app.py`.
- Imports trocados para relativos (`from . import ...`, `from ..src.etl import ...`), para funcionarem dentro de pacotes.
- **Seção 1:** a mensagem de erro que citava `gerar_dados_exemplo.py` foi trocada por instrução de upload, porque o gerador não faz parte do painel.
- **Seção 3:** a imagem ausente e o CSV de evolução ausente passaram a mostrar aviso, em vez de derrubar as abas seguintes.
- **Seção 2 e 4:** o código de página foi colocado dentro de `render()`, sem mudar a lógica.

## Antes de entregar (checklist)

- [ ] `streamlit run app.py` abre e as seis opções do menu carregam.
- [x] Base real do Censo 2022 incluída na seção 1.
- [x] Imagens da seção 3 colocadas em `secoes/aluno3_indigenas/assets/`.
- [x] Valores por UF da seção 4 conferidos no SIDRA.
- [ ] Convenção do desvio padrão decidida e registrada.
- [ ] Nomes dos integrantes preenchidos.
- [ ] Subir no GitHub sem a pasta `.venv` (o `.gitignore` já cuida disso).
