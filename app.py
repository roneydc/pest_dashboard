"""
Ponto de entrada principal para o Dashboard PT201
Inicializa e executa o aplicativo Dash
"""
import dash
import dash_bootstrap_components as dbc
import socket
import warnings
warnings.filterwarnings('ignore')

from config import DATA_PATH, SHAPEFILE_PATH, APP_HOST, APP_PORT, APP_DEBUG, APP_TITLE, THEME

from data.data_loader import DataLoader
from data.data_processor import DataProcessor
from data.geo_loader import GeoLoader
from layouts.main_layout import MainLayout
from callbacks.callback_manager import CallbackManager
from callbacks.update_graphs import GraphUpdater


class DashboardApp:
    """Classe principal que coordena o Dashboard PT201"""
    
    def __init__(self):
        """Inicializa o aplicativo Dashboard PT201"""
        self.app = None
        self.data_loader = None
        self.data_processor = None
        self.geo_loader = None
        
    def initialize(self):
        """Inicializa todos os componentes do dashboard"""
        print("🔄 Inicializando componentes do dashboard...")
        
        # Inicializar carregadores de dados
        self.data_loader = DataLoader(DATA_PATH)
        self.data_processor = DataProcessor()
        self.geo_loader = GeoLoader(SHAPEFILE_PATH)
        
        # Carregar dados
        processed_df = self.data_loader.load_data()
        if not self.data_loader.validate_data():
            print("❌ Falha ao carregar dados. Encerrando aplicação.")
            exit(1)
            
        # Processar dados
        print("🔄 Preparando dados para visualização...")
        self.data_processor.set_data(processed_df)
        processed_df = self.data_processor.process_dates()

        # Verificar se as colunas necessárias foram criadas
        if 'year' not in processed_df.columns:
            print("⚠️ Aviso: Coluna 'year' não foi criada. Criando com valores padrão...")
            processed_df['year'] = 2023
            self.data_processor.set_data(processed_df)
        
        # Carregar dados geográficos
        self.geo_loader.load_shapefile()
        
        # Obter parâmetros para o layout
        field_options, crop_options, pest_options = self.data_processor.get_dropdown_options()
        most_recent_year = self.data_processor.get_most_recent_year()
        first_field = self.data_processor.get_first_field()
        year_min = processed_df['year'].min() if 'year' in processed_df else 2020
        year_max = processed_df['year'].max() if 'year' in processed_df else 2023
        
        # Inicializar o App Dash
        self.app = dash.Dash(
            __name__, 
            external_stylesheets=[getattr(dbc.themes, THEME)],
            title=APP_TITLE
        )
        
        # Criar layout
        layout = MainLayout(
            year_min,
            year_max,
            most_recent_year,
            field_options,
            crop_options,
            pest_options,
            first_field
        )
        self.app.layout = layout.create()
        
        # Configurar callbacks
        graph_updater = GraphUpdater(self.data_processor, self.geo_loader)
        callback_manager = CallbackManager(self.app, graph_updater)
        callback_manager.register_callbacks()
        
        print("✅ Dashboard inicializado com sucesso!")
        
    def run(self):
        """Executa o servidor Dash"""
        if self.app is None:
            self.initialize()
            
        most_recent_year = self.data_processor.get_most_recent_year()
        print("🚀 Iniciando o dashboard PT201...")
        print(f"📊 Mostrando dados iniciais apenas para o ano mais recente: {most_recent_year}")
        
        # Imprimir informações de acesso
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"\n✅ Dashboard pronto! Acesse em um dos seguintes endereços:")
        print(f"   - Local: http://127.0.0.1:{APP_PORT}")
        print(f"   - Rede: http://{local_ip}:{APP_PORT}")
        
        # Iniciar o servidor
        self.app.run(host=APP_HOST, debug=APP_DEBUG, port=APP_PORT)


if __name__ == '__main__':
    dashboard = DashboardApp()
    dashboard.run()