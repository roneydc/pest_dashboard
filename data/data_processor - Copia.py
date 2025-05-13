"""
Classe para processamento de dados do Dashboard PT201
"""
import pandas as pd
import numpy as np
from datetime import datetime
from config import MONTH_ORDER, MAX_TOP_ITEMS

class DataProcessor:
    """Classe responsável pelo processamento de dados"""
    
    def __init__(self, df=None):
        """
        Inicializa o processador de dados
        
        Args:
            df (pandas.DataFrame, optional): DataFrame inicial. Defaults to None.
        """
        self.df = df
        self.filtered_df = None
    
    def set_data(self, df):
        """
        Define o DataFrame a ser processado
        
        Args:
            df (pandas.DataFrame): DataFrame a ser processado
        """
        self.df = df
        
    def process_dates(self):
        """
        Processa colunas de data no DataFrame
        
        Returns:
            pandas.DataFrame: DataFrame com colunas de data processadas
        """
        if self.df is None:
            return None
            
        df = self.df.copy()
        
        try:
            # Converter colunas de data
            df['start_time'] = pd.to_datetime(df['start_time'], format='mixed', errors='coerce')
            
            # Adicionar colunas derivadas para filtragem temporal
            df['year'] = df['start_time'].dt.year
            df['month'] = df['start_time'].dt.month
            df['month_name'] = df['start_time'].dt.strftime('%b')
            df['month_year'] = df['start_time'].dt.strftime('%Y-%m')
            
            print("✅ Datas convertidas e colunas temporais criadas")
            
        except Exception as e:
            print(f"⚠️ Aviso na conversão de datas: {str(e)}")
            # Criar colunas vazias para não quebrar o dashboard
            df['year'] = 2023
            df['month'] = 1
            df['month_name'] = 'Jan'
            df['month_year'] = '2023-01'
        
        # Atualizar o DataFrame interno da classe
        self.df = df
        return df
        
    def get_dropdown_options(self, df=None):
        """
        Obtém opções para os dropdowns do dashboard
        
        Args:
            df (pandas.DataFrame, optional): DataFrame a ser usado. 
                                            Se None, usa o df da classe. Defaults to None.
        
        Returns:
            tuple: Tupla contendo (field_options, crop_options, pest_options)
        """
        if df is None:
            df = self.df
            
        if df is None or len(df) == 0:
            return [], [], []
            
        # Preparar opções para dropdown de campos
        field_options = [{'label': field, 'value': field} 
                        for field in sorted(df['loc_name'].unique())]

        # Preparar opções para dropdown de culturas
        crop_options = [{'label': crop, 'value': crop} 
                        for crop in sorted(df['et_name_crop'].unique())]

        # Preparar opções para dropdown de pragas
        pest_options = [{'label': pest, 'value': pest} 
                        for pest in sorted(df['et_name_pest'].unique())]
                        
        return field_options, crop_options, pest_options
        
    def get_first_field(self):
        """
        Obtém o primeiro campo por ordem alfabética
        
        Returns:
            str: Nome do primeiro campo ou None se não houver campos
        """
        if self.df is None or len(self.df) == 0 or 'loc_name' not in self.df.columns:
            return None
            
        fields = sorted(self.df['loc_name'].unique())
        return fields[0] if fields else None
        
    def get_most_recent_year(self):
        """
        Obtém o ano mais recente no DataFrame
        
        Returns:
            int: Ano mais recente ou None se não houver dados
        """
        if self.df is None or len(self.df) == 0 or 'year' not in self.df.columns:
            return None
            
        return self.df['year'].max()
        
    def apply_filters(self, year_range=None, fields=None, crops=None, pests=None):
        """
        Aplica filtros aos dados
        
        Args:
            year_range (list, optional): Intervalo de anos [min, max]. Defaults to None.
            fields (list, optional): Lista de campos. Defaults to None.
            crops (list, optional): Lista de culturas. Defaults to None.
            pests (list, optional): Lista de pragas. Defaults to None.
            
        Returns:
            pandas.DataFrame: DataFrame filtrado
        """
        if self.df is None:
            return pd.DataFrame()
            
        filtered_df = self.df.copy()
        
        # Aplicar filtros
        if year_range:
            filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & 
                                    (filtered_df['year'] <= year_range[1])]
        
        if fields and len(fields) > 0:
            filtered_df = filtered_df[filtered_df['loc_name'].isin(fields)]
        
        if crops and len(crops) > 0:
            filtered_df = filtered_df[filtered_df['et_name_crop'].isin(crops)]
        
        if pests and len(pests) > 0:
            filtered_df = filtered_df[filtered_df['et_name_pest'].isin(pests)]
            
        self.filtered_df = filtered_df
        return filtered_df
        
    def get_kpi_data(self):
        """
        Calcula dados para KPIs
        
        Returns:
            tuple: (total_monitoring, unique_fields, main_crop)
        """
        if self.filtered_df is None or len(self.filtered_df) == 0:
            return 0, 0, "N/A"
            
        # KPIs
        total_monitoring = len(self.filtered_df)
        unique_fields = self.filtered_df['loc_name'].nunique()
        
        # Cultura principal
        if len(self.filtered_df) > 0 and 'et_name_crop' in self.filtered_df.columns:
            main_crop = self.filtered_df['et_name_crop'].value_counts().index[0]
            main_crop_short = main_crop[:15] + "..." if len(main_crop) > 15 else main_crop
        else:
            main_crop_short = "N/A"
            
        return total_monitoring, unique_fields, main_crop_short
        
    def get_time_trend_data(self):
        """
        Obtém dados para gráfico de tendência temporal
        
        Returns:
            pandas.DataFrame: DataFrame com dados de tendência temporal
        """
        if self.filtered_df is None or len(self.filtered_df) == 0:
            return pd.DataFrame()
            
        # Gráfico 1: Tendência Temporal
        time_data = self.filtered_df.groupby('month_year').size().reset_index(name='count')
        
        # Ordenar por data
        time_data['date_sort'] = pd.to_datetime(time_data['month_year'], format='%Y-%m')
        time_data = time_data.sort_values('date_sort')
        
        return time_data
        
    def get_pest_distribution(self):
        """
        Obtém dados para gráfico de distribuição de pragas
        
        Returns:
            pandas.DataFrame: DataFrame com distribuição de pragas
        """
        if self.filtered_df is None or len(self.filtered_df) == 0:
            return pd.DataFrame()
            
        # Distribuição de Pragas
        pest_counts = self.filtered_df['et_name_pest'].value_counts().reset_index()
        pest_counts.columns = ['et_name_pest', 'count']
        pest_counts = pest_counts.sort_values('count', ascending=False).head(MAX_TOP_ITEMS)
        
        return pest_counts
        
    def get_field_analysis(self):
        """
        Obtém dados para análise por campo
        
        Returns:
            pandas.DataFrame: DataFrame com análise por campo
        """
        if self.filtered_df is None or len(self.filtered_df) == 0:
            return pd.DataFrame()
            
        # Análise por Campo
        field_analysis = self.filtered_df.groupby('loc_name').size().reset_index(name='count')
        field_analysis = field_analysis.sort_values('count', ascending=False).head(MAX_TOP_ITEMS)
        
        return field_analysis
        
    def get_crop_severity(self):
        """
        Obtém dados para análise de severidade por cultura
        
        Returns:
            tuple: (pandas.DataFrame, str) - (dados, nome da coluna de severidade)
        """
        if self.filtered_df is None or len(self.filtered_df) == 0:
            return pd.DataFrame(), None
            
        # Usar scale ou data_grade como proxy de severidade
        severity_col = None
        for col in ['scale', 'data_grade', 'data_number']:
            if col in self.filtered_df.columns and not self.filtered_df[col].isnull().all():
                severity_col = col
                break
        
        if severity_col:
            crop_severity = self.filtered_df.groupby('et_name_crop')[severity_col].mean().reset_index()
            crop_severity = crop_severity.sort_values(severity_col, ascending=False).head(MAX_TOP_ITEMS)
            return crop_severity, severity_col
        else:
            return pd.DataFrame(), None
            
    def get_monthly_severity(self):
        """
        Obtém dados para análise de severidade mensal
        
        Returns:
            tuple: (pandas.DataFrame, str) - (dados, nome da coluna de severidade)
        """
        if self.filtered_df is None or len(self.filtered_df) == 0:
            return pd.DataFrame(), None
            
        # Usar scale ou data_grade como proxy de severidade
        severity_col = None
        for col in ['scale', 'data_grade', 'data_number']:
            if col in self.filtered_df.columns and not self.filtered_df[col].isnull().all():
                severity_col = col
                break
                
        if severity_col and 'month_name' in self.filtered_df.columns:
            monthly_severity = self.filtered_df.groupby('month_name')[severity_col].agg(['mean', 'max']).reset_index()
            
            # Ordenar meses corretamente
            monthly_severity['month_num'] = monthly_severity['month_name'].apply(
                lambda x: MONTH_ORDER.index(x) if x in MONTH_ORDER else -1
            )
            monthly_severity = monthly_severity.sort_values('month_num')
            
            return monthly_severity, severity_col
        else:
            return pd.DataFrame(), None
            
    def get_cooccurrence_data(self):
        """
        Obtém dados para matriz de co-ocorrência Praga-Cultura
        
        Returns:
            tuple: (z_data, x_data, y_data) para o heatmap
        """
        if self.filtered_df is None or len(self.filtered_df) == 0:
            return None, None, None
            
        # Obter top pragas e culturas
        top_pests = self.filtered_df['et_name_pest'].value_counts().head(6).index
        top_crops = self.filtered_df['et_name_crop'].value_counts().head(6).index
        
        # Filtrar dados para essas pragas e culturas
        subset = self.filtered_df[
            self.filtered_df['et_name_pest'].isin(top_pests) & 
            self.filtered_df['et_name_crop'].isin(top_crops)
        ]
        
        if len(subset) == 0:
            return None, None, None
            
        # Criar tabela de contingência
        crosstab = pd.crosstab(subset['et_name_pest'], subset['et_name_crop'])
        
        # Converter para formato para plotly
        z_data = crosstab.values
        x_data = crosstab.columns.tolist()
        y_data = crosstab.index.tolist()
        
        return z_data, x_data, y_data