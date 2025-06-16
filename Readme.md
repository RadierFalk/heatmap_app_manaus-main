# Documentação da Aplicação Web para Mapeamento de Ilhas de Calor em Manaus

## Visão Geral

Esta aplicação web foi desenvolvida para mapear ilhas de calor em Manaus, Amazonas, e identificar locais estratégicos para intervenções sustentáveis como jardins verticais e telhados verdes. A aplicação utiliza dados meteorológicos e técnicas de visualização geoespacial para criar mapas de calor interativos que auxiliam no planejamento urbano sustentável.

## Funcionalidades

- **Visualização de Mapas de Calor**: Geração de mapas de calor baseados em dados meteorológicos para Manaus.
- **Análise por Período**: Seleção de períodos específicos para análise das condições climáticas.
- **Múltiplos Fatores Ambientais**: Análise de diferentes fatores como temperatura, umidade e precipitação.
- **Identificação de Locais para Intervenção**: Marcação automática de locais potenciais para implementação de infraestrutura verde.
- **Estatísticas Detalhadas**: Apresentação de estatísticas sobre os dados analisados.
- **Interface Responsiva**: Design adaptável a diferentes dispositivos.

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Dados Meteorológicos**: Meteostat
- **Visualização de Mapas**: Folium (baseado em Leaflet.js)
- **Análise de Dados**: Pandas, NumPy
- **Dados Geoespaciais**: GeoPandas
- **Frontend**: HTML, CSS, Bootstrap

## Estrutura do Projeto

```
heatmap_app/
├── venv/                  # Ambiente virtual Python
├── src/                   # Código-fonte da aplicação
│   ├── main.py            # Arquivo principal da aplicação Flask
│   ├── static/            # Arquivos estáticos (CSS, JS, imagens)
│   └── templates/         # Templates HTML
│       ├── index.html     # Página inicial
│       └── heatmap_result.html  # Página de resultados
└── requirements.txt       # Dependências do projeto
```

## Como Executar a Aplicação

1. Certifique-se de ter Python 3.6+ instalado
2. Clone o repositório ou extraia os arquivos
3. Navegue até a pasta do projeto
4. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
5. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
6. Execute a aplicação:
   ```
   cd src
   python main.py
   ```
7. Acesse a aplicação em seu navegador: `http://127.0.0.1:5000`

## Uso da Aplicação

1. Na página inicial, você verá um mapa base de Manaus e um formulário para gerar o mapa de calor.
2. Selecione o período de análise usando os campos de data inicial e final.
3. Escolha o fator ambiental que deseja analisar (temperatura, umidade ou precipitação).
4. Clique em "Gerar Mapa" para criar o mapa de calor.
5. Na página de resultados, você verá:
   - O mapa de calor com áreas críticas destacadas
   - Marcadores verdes indicando locais potenciais para intervenções sustentáveis
   - Estatísticas sobre o período analisado
   - Recomendações para implementação de infraestrutura verde

## Personalização

A aplicação pode ser personalizada para incluir:
- Dados meteorológicos mais detalhados ou de outras fontes
- Análise de fatores ambientais adicionais
- Integração com sistemas de informação geográfica (GIS)
- Expansão para outras cidades além de Manaus

## Limitações Atuais

- Os dados são simulados com base em médias reais para demonstração
- Para uma implementação em produção, recomenda-se a integração com fontes de dados meteorológicos em tempo real
- A precisão da identificação de locais para intervenção pode ser aprimorada com dados mais granulares

## Próximos Passos Sugeridos

- Integração com APIs meteorológicas em tempo real
- Adição de camadas de dados sobre vegetação existente e densidade populacional
- Implementação de algoritmos de aprendizado de máquina para previsão de tendências
- Desenvolvimento de recursos para comparação entre diferentes períodos
- Criação de relatórios exportáveis para planejamento urbano

## Contato e Suporte

Para dúvidas, sugestões ou problemas, entre em contato através do email: [seu-email@exemplo.com]
