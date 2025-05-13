"""
Gerenciador central de callbacks do Dashboard PT201
"""
from dash import Input, Output, State, callback

from callbacks.update_graphs import GraphUpdater

class CallbackManager:
    """Classe para gerenciar os callbacks do dashboard"""
    
    def __init__(self, app, graph_updater):
        """
        Inicializa o gerenciador de callbacks
        
        Args:
            app (dash.Dash): Aplicação Dash
            graph_updater (GraphUpdater): Atualizador de gráficos
        """
        self.app = app
        self.graph_updater = graph_updater
        
    def register_callbacks(self):
        """Registra todos os callbacks necessários para o dashboard"""
        self._register_main_callback()
        self._register_initialization_callback()
        
    def _register_main_callback(self):
        """Registra o callback principal que atualiza todos os gráficos"""
        @self.app.callback(
            [Output("kpi-total", "children"),
             Output("kpi-fields", "children"),
             Output("kpi-main-crop", "children"),
             Output("time-trend", "figure"),
             Output("geo-map", "figure"),
             Output("pest-distribution", "figure"),
             Output("field-analysis", "figure"),
             Output("crop-severity", "figure"),
             Output("severity-analysis", "figure"),
             Output("co-occurrence", "figure")],
            [Input("apply-filters", "n_clicks")],
            [State("year-filter", "value"),
             State("field-filter", "value"),
             State("crop-filter", "value"),
             State("pest-filter", "value")]
        )
        def update_dashboard(n_clicks, year_range, fields, crops, pests):
            """
            Callback que atualiza todos os gráficos quando os filtros são aplicados
            
            Args:
                n_clicks (int): Número de cliques no botão
                year_range (list): Intervalo de anos selecionado
                fields (list): Campos selecionados
                crops (list): Culturas selecionadas
                pests (list): Pragas selecionadas
                
            Returns:
                tuple: Todos os outputs atualizados
            """
            return self.graph_updater.update_all_graphs(year_range, fields, crops, pests)
        
    def _register_initialization_callback(self):
        """Registra o callback de inicialização do dashboard"""
        @self.app.callback(
            Output("apply-filters", "n_clicks"),
            [Input("field-filter", "options")]
        )
        def initialize_dashboard(options):
            """
            Callback que inicializa o dashboard automaticamente
            
            Args:
                options (list): Opções do dropdown de campos
                
            Returns:
                int: 1 para simular um clique no botão
            """
            return 1