"""
Componente do painel de filtros para o Dashboard PT201
"""
import dash_bootstrap_components as dbc
from dash import dcc, html

class FilterPanel:
    """Classe para criar o painel de filtros"""
    
    def __init__(self, year_min, year_max, most_recent_year, field_options, crop_options, pest_options, first_field):
        """
        Inicializa o painel de filtros
        
        Args:
            year_min (int): Ano mínimo para o filtro
            year_max (int): Ano máximo para o filtro
            most_recent_year (int): Ano mais recente para valor padrão
            field_options (list): Lista de opções para o dropdown de campos
            crop_options (list): Lista de opções para o dropdown de culturas
            pest_options (list): Lista de opções para o dropdown de pragas
            first_field (str): Primeiro campo para seleção padrão
        """
        self.year_min = year_min
        self.year_max = year_max
        self.most_recent_year = most_recent_year
        self.field_options = field_options
        self.crop_options = crop_options
        self.pest_options = pest_options
        self.first_field = first_field
    
    def create(self):
        """
        Cria o painel de filtros
        
        Returns:
            dash_bootstrap_components.Col: Componente do painel de filtros
        """
        return dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filtros", className="text-center"),
                dbc.CardBody([
                    html.Label("Período de Tempo:"),
                    dcc.RangeSlider(
                        id="year-filter",
                        min=self.year_min if self.year_min else 2020,
                        max=self.year_max if self.year_max else 2023,
                        # Iniciar com apenas o ano mais recente selecionado
                        value=[self.most_recent_year, self.most_recent_year] if self.most_recent_year else [2023, 2023],
                        marks={str(year): str(year) for year in range(
                            self.year_min if self.year_min else 2020, 
                            (self.year_max if self.year_max else 2023) + 1
                        )},
                        step=1
                    ),
                    html.Br(),
                    
                    html.Label("Campo:"),
                    dcc.Dropdown(
                        id="field-filter",
                        options=self.field_options,
                        value=[self.first_field] if self.first_field else None,
                        multi=True,
                        placeholder="Selecione um ou mais campos"
                    ),
                    html.Br(),
                    
                    html.Label("Cultura:"),
                    dcc.Dropdown(
                        id="crop-filter",
                        options=self.crop_options,
                        multi=True,
                        placeholder="Selecione uma ou mais culturas"
                    ),
                    html.Br(),
                    
                    html.Label("Tipo de Praga:"),
                    dcc.Dropdown(
                        id="pest-filter",
                        options=self.pest_options,
                        multi=True,
                        placeholder="Selecione um ou mais tipos de pragas"
                    ),
                    html.Br(),
                    
                    dbc.Button("Aplicar Filtros", id="apply-filters", color="primary", className="w-100")
                ])
            ])
        ], width=3)