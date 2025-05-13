"""
Componente para cartões de KPI
"""
import dash_bootstrap_components as dbc
from dash import html

class KPICards:
    """Classe para criar os cartões de KPI"""
    
    @staticmethod
    def create():
        """
        Cria o componente de cartões KPI
        
        Returns:
            dash_bootstrap_components.Row: Linha com os cartões KPI
        """
        return dbc.Row([
            # KPI Total de Monitoramentos
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total de Monitoramentos", className="card-title text-center"),
                        html.H2(id="kpi-total", className="text-center text-primary")
                    ])
                ])
            ], width=4),
            
            # KPI Campos Monitorados
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Campos Monitorados", className="card-title text-center"),
                        html.H2(id="kpi-fields", className="text-center text-success")
                    ])
                ])
            ], width=4),
            
            # KPI Cultura Principal
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Cultura Principal", className="card-title text-center"),
                        html.H2(id="kpi-main-crop", className="text-center text-info")
                    ])
                ])
            ], width=4)
        ])