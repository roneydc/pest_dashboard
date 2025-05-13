"""
Componente de cabeçalho para o Dashboard PT201
"""
import dash_bootstrap_components as dbc
from dash import html
from config import APP_TITLE, APP_SUBTITLE

class Header:
    """Classe para criar o componente de cabeçalho"""
    
    @staticmethod
    def create():
        """
        Cria o componente de cabeçalho
        
        Returns:
            dash_bootstrap_components.Row: Componente de cabeçalho
        """
        return dbc.Row([
            dbc.Col([
                html.H1(APP_TITLE, className="text-center mb-4"),
                html.H5(APP_SUBTITLE, className="text-center text-muted mb-4")
            ], width=12)
        ])