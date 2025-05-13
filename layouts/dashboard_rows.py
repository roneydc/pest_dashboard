"""
Componente para as linhas do dashboard
"""
import dash_bootstrap_components as dbc
from dash import dcc, html

class DashboardRows:
    """Classe para criar as linhas do dashboard"""
    
    @staticmethod
    def create_time_trend_row():
        """
        Cria a linha com o gráfico de tendência temporal
        
        Returns:
            dash_bootstrap_components.Card: Cartão com o gráfico
        """
        return dbc.Card([
            dbc.CardHeader("Tendência Temporal de Monitoramentos", className="text-center"),
            dbc.CardBody([
                dcc.Graph(id="time-trend")
            ])
        ])
    
    @staticmethod
    def create_map_and_pest_row():
        """
        Cria a linha com o mapa e distribuição de pragas
        
        Returns:
            dash_bootstrap_components.Row: Linha com os gráficos
        """
        return dbc.Row([
            # Mapa de distribuição
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribuição Geográfica", className="text-center"),
                    dbc.CardBody([
                        dcc.Graph(id="geo-map")
                    ])
                ])
            ], width=6),
            
            # Distribuição de pragas
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Principais Tipos de Pragas PT201", className="text-center"),
                    dbc.CardBody([
                        dcc.Graph(id="pest-distribution")
                    ])
                ])
            ], width=6)
        ])
    
    @staticmethod
    def create_field_and_crop_row():
        """
        Cria a linha com análise por campo e cultura
        
        Returns:
            dash_bootstrap_components.Row: Linha com os gráficos
        """
        return dbc.Row([
            # Análise por campo
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Top 10 Campos com Maior Incidência", className="text-center"),
                    dbc.CardBody([
                        dcc.Graph(id="field-analysis")
                    ])
                ])
            ], width=6),
            
            # Cultura x Severidade
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Severidade por Cultura", className="text-center"),
                    dbc.CardBody([
                        dcc.Graph(id="crop-severity")
                    ])
                ])
            ], width=6)
        ])
    
    @staticmethod
    def create_severity_and_cooccurrence_row():
        """
        Cria a linha com análise de severidade e matriz de correlação
        
        Returns:
            dash_bootstrap_components.Row: Linha com os gráficos
        """
        return dbc.Row([
            # Análise de severidade
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Análise de Severidade Mensal", className="text-center"),
                    dbc.CardBody([
                        dcc.Graph(id="severity-analysis")
                    ])
                ])
            ], width=6),
            
            # Matriz de correlação praga-campo
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Co-ocorrência Praga-Cultura", className="text-center"),
                    dbc.CardBody([
                        dcc.Graph(id="co-occurrence")
                    ])
                ])
            ], width=6)
        ])