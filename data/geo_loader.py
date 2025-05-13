"""
Classe para carregamento e processamento de dados geográficos
"""
import geopandas as gpd
import json
import pandas as pd
import numpy as np

class GeoLoader:
    """Classe responsável por carregar e processar dados geográficos"""
    
    def __init__(self, shapefile_path):
        """
        Inicializa o carregador de dados geográficos
        
        Args:
            shapefile_path (str): Caminho para o arquivo shapefile
        """
        self.shapefile_path = shapefile_path
        self.gdf = None
        self.geojson = None
    
    def load_shapefile(self):
        """
        Carrega o shapefile com os limites dos campos
        
        Returns:
            dict: GeoJSON convertido a partir do shapefile ou None em caso de erro
        """
        try:
            # Carregar o shapefile
            self.gdf = gpd.read_file(self.shapefile_path)
            
            # Verificar e transformar para WGS84 (sistema de coordenadas usado pelo Mapbox)
            if self.gdf.crs != 'EPSG:4326':
                self.gdf = self.gdf.to_crs('EPSG:4326')
            
            # Converter para GeoJSON
            self.geojson = json.loads(self.gdf.to_json())
            
            print(f"✅ Shapefile carregado: {len(self.gdf)} polígonos de campos")
            return self.geojson
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar shapefile: {str(e)}")
            self.geojson = None
            return None
    
    def process_geo_data(self, df):
        """
        Processa dados geográficos a partir do DataFrame
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados a serem processados
        
        Returns:
            pandas.DataFrame: DataFrame filtrado contendo apenas dados geográficos válidos
        """
        # Filtrar valores inválidos nas coordenadas geográficas
        df_geo = df.copy()
        df_geo = df_geo.dropna(subset=['latitude', 'longitude'])
        df_geo = df_geo[(df_geo['latitude'] >= -90) & (df_geo['latitude'] <= 90)]
        df_geo = df_geo[(df_geo['longitude'] >= -180) & (df_geo['longitude'] <= 180)]
        
        return df_geo
    
    def get_field_counts(self, df):
        """
        Calcula a contagem de ocorrências por campo
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados
            
        Returns:
            pandas.DataFrame: DataFrame com contagem agrupada por campo
        """
        # Verificar se há dados geográficos
        if df is None or len(df) == 0:
            return pd.DataFrame()
            
        # Agrupar por campo para o mapa
        field_counts = df.groupby('loc_name').agg({
            'id': 'count',
            'latitude': 'mean',
            'longitude': 'mean'
        }).reset_index()
        
        field_counts.rename(columns={'id': 'count'}, inplace=True)
        return field_counts
    
    def get_geojson(self):
        """
        Retorna o GeoJSON carregado
        
        Returns:
            dict: GeoJSON ou None se não estiver carregado
        """
        if self.geojson is None:
            self.load_shapefile()
        return self.geojson