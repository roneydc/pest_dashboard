"""
Componente de rodapé para o Dashboard PT201
"""
import dash_bootstrap_components as dbc
from dash import html
from config import APP_FOOTER

class Footer:
    """Classe para criar o componente de rodapé"""
    
    @staticmethod
    def create():
        """
        Cria o componente de rodapé
        
        Returns:
            dash_bootstrap_components.Row: Componente de rodapé
        """
        return dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P(APP_FOOTER, className="text-center text-muted"),
            ], width=12)
        ])