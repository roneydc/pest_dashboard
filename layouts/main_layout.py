"""
Layout principal do Dashboard PT201
"""
import dash_bootstrap_components as dbc
from dash import html

from components.header import Header
from components.footer import Footer
from components.filter_panel import FilterPanel
from layouts.kpi_cards import KPICards
from layouts.dashboard_rows import DashboardRows

class MainLayout:
    """Classe para criar o layout principal do dashboard"""
    
    def __init__(self, year_min, year_max, most_recent_year, field_options, crop_options, pest_options, first_field):
        """
        Inicializa o layout principal
        
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
        Cria o layout principal do dashboard
        
        Returns:
            dash_bootstrap_components.Container: Container principal do dashboard
        """
        # Criar o painel de filtros
        filter_panel = FilterPanel(
            self.year_min,
            self.year_max,
            self.most_recent_year,
            self.field_options,
            self.crop_options,
            self.pest_options,
            self.first_field
        ).create()
        
        # Criar o layout com todos os componentes
        return dbc.Container([
            # Cabeçalho
            Header.create(),
            
            # Filtros e KPIs
            dbc.Row([
                # Painel de filtros
                filter_panel,
                
                # Painel com KPIs e gráfico temporal
                dbc.Col([
                    # KPIs
                    KPICards.create(),
                    
                    html.Br(),
                    
                    # Gráfico de tendência temporal
                    DashboardRows.create_time_trend_row()
                ], width=9)
            ]),
            
            html.Br(),
            
            # Segunda linha - Mapa e Distribuição
            DashboardRows.create_map_and_pest_row(),
            
            html.Br(),
            
            # Terceira linha - Análise por campo e cultura
            DashboardRows.create_field_and_crop_row(),
            
            html.Br(),
            
            # Quarta linha - Análise de Severidade e Matriz de correlação
            DashboardRows.create_severity_and_cooccurrence_row(),
            
            # Rodapé
            Footer.create()
            
        ], fluid=True)