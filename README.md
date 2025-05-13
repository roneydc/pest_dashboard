# Dashboard PT201 - Documentação

## Visão Geral

O Dashboard PT201 é uma aplicação web desenvolvida com Dash para monitoramento e análise de pragas em campos agrícolas. Esta refatoração modulariza o código original em uma estrutura orientada a objetos que facilita a manutenção e extensão do sistema.

## Estrutura do Código

O projeto foi modularizado seguindo os princípios de Programação Orientada a Objetos (POO), com separação clara de responsabilidades:

- **app.py**: Ponto de entrada da aplicação que coordena a inicialização e execução do dashboard
- **config.py**: Configurações globais da aplicação (caminhos, constantes, esquemas de cores)

### Pacotes Principais

#### data/
Módulos para carregamento e processamento de dados:
- **data_loader.py**: Carrega dados do arquivo CSV
- **data_processor.py**: Processa, filtra e agrega dados para visualização
- **geo_loader.py**: Carrega e processa dados geográficos (shapefiles)

#### components/
Componentes de interface reutilizáveis:
- **header.py**: Cabeçalho da aplicação
- **footer.py**: Rodapé da aplicação
- **filter_panel.py**: Painel de filtros do dashboard

#### layouts/
Estruturas de layout que compõem a interface:
- **main_layout.py**: Layout principal que integra todos os componentes
- **kpi_cards.py**: Cartões de indicadores-chave de desempenho
- **dashboard_rows.py**: Linhas de gráficos do dashboard

#### visualizations/
Classes especializadas para criar visualizações:
- **time_series.py**: Gráficos de séries temporais
- **geographic.py**: Visualizações geográficas (mapas)
- **distribution.py**: Gráficos de distribuição
- **correlation.py**: Gráficos de correlação (heatmaps)

#### callbacks/
Gerenciamento de interatividade:
- **callback_manager.py**: Gerencia todos os callbacks da aplicação
- **update_graphs.py**: Funções para atualizar gráficos com base nos filtros

## Fluxo de Execução

1. O arquivo `app.py` inicializa a aplicação, através da classe `DashboardApp`.
2. Os dados são carregados via `DataLoader` e processados via `DataProcessor`.
3. Os dados geográficos são carregados através do `GeoLoader`.
4. O layout é criado através da classe `MainLayout`, que integra todos os componentes.
5. Os callbacks são registrados pelo `CallbackManager`.
6. O servidor Dash é iniciado para servir a aplicação.

## Como Executar

```bash
python app.py
```

A aplicação estará disponível em:
- Local: http://127.0.0.1:8050
- Rede: http://[seu-ip]:8050


## Diagrama de Classes

```
DashboardApp
├── DataLoader
├── DataProcessor
├── GeoLoader
├── MainLayout
│   ├── Header
│   ├── FilterPanel
│   ├── KPICards
│   └── DashboardRows
└── CallbackManager
    └── GraphUpdater
        ├── TimeSeriesVisualizer
        ├── GeographicVisualizer
        ├── DistributionVisualizer
        └── CorrelationVisualizer
```