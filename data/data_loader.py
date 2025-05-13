"""
Classe para carregamento de dados do Dashboard PT201
"""
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataLoader:
    """Classe responsável por carregar e realizar pré-processamento inicial dos dados"""
    
    def __init__(self, file_path):
        """
        Inicializa o carregador de dados
        
        Args:
            file_path (str): Caminho para o arquivo CSV de dados
        """
        self.file_path = file_path
        self.df = None
    
    def load_data(self):
        """
        Carrega os dados do arquivo CSV
        
        Returns:
            pandas.DataFrame: DataFrame com os dados carregados ou DataFrame vazio em caso de erro
        """
        print("🔄 Iniciando carregamento dos dados PT201...")
        
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"✅ Dados carregados: {len(self.df)} registros, {len(self.df.columns)} colunas")
            return self.df
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {str(e)}")
            # Se falhar, criar DataFrame vazio para evitar quebrar o código
            self.df = pd.DataFrame()
            return self.df
    
    def validate_data(self):
        """
        Valida se os dados foram carregados corretamente
        
        Returns:
            bool: True se dados forem válidos, False caso contrário
        """
        # Verificar se temos dados
        if self.df is None or len(self.df) == 0:
            print("❌ Nenhum dado encontrado. Verifique o caminho do arquivo.")
            return False
        return True
    
    def get_data(self):
        """
        Retorna os dados carregados
        
        Returns:
            pandas.DataFrame: DataFrame com os dados carregados
        """
        if self.df is None:
            self.load_data()
        return self.df