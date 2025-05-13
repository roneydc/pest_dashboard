"""
Arquivo de configuração para o Dashboard PT201
Contém constantes e configurações globais
"""

# Configurações de arquivos
#DATA_PATH = 'D:/dados_agritask/pest_data_by_code/pest_code_PT201.csv'
DATA_PATH = 'D:/dados_agritask/pest_code_resume_PT201.csv'
SHAPEFILE_PATH = 'D:/Imagens_Planet/Indices semanais/Bando_Imagens/Limites/Grupo Bom Jesus (1)/Grupo Bom Jesus.shp'

# Configurações do servidor
APP_HOST = '0.0.0.0'
APP_PORT = 8050
APP_DEBUG = False

# Configurações de estilo
THEME = 'BOOTSTRAP'
COLOR_SCHEMES = {
    'primary': 'Blues',
    'secondary': 'Greens',
    'success': 'Viridis',
    'danger': 'Reds',
    'warning': 'Oranges',
    'info': 'YlGnBu'
}

# Configurações de visualização
MAX_TOP_ITEMS = 10
MAPBOX_STYLE = "carto-positron"
MONTH_ORDER = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Textos do aplicativo
APP_TITLE = "Dashboard PT201 - Análise de Pragas"
APP_SUBTITLE = "Monitoramento de Pragas em Campos Agrícolas"
APP_FOOTER = "Dashboard de Monitoramento PT201 © 2025"