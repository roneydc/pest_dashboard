"""
Funções para atualizar gráficos no Dashboard PT201
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from visualizations.time_series import TimeSeriesVisualizer
from visualizations.geographic import GeographicVisualizer
from visualizations.distribution import DistributionVisualizer
from visualizations.correlation import CorrelationVisualizer

class GraphUpdater:
    """Classe para atualizar gráficos com base nos dados filtrados"""
    
    def __init__(self, data_processor, geo_loader):
        """
        Inicializa o atualizador de gráficos
        
        Args:
            data_processor (DataProcessor): Processador de dados
            geo_loader (GeoLoader): Carregador de dados geográficos
        """
        self.data_processor = data_processor
        self.geo_loader = geo_loader
        
    def update_all_graphs(self, year_range, fields, crops, pests):
        """
        Atualiza todos os gráficos com base nos filtros selecionados
        
        Args:
            year_range (list): Intervalo de anos [min, max]
            fields (list): Lista de campos selecionados
            crops (list): Lista de culturas selecionadas
            pests (list): Lista de pragas selecionadas
            
        Returns:
            tuple: Tupla com todos os valores atualizados para os gráficos
        """
        # Aplicar filtros
        filtered_df = self.data_processor.apply_filters(year_range, fields, crops, pests)
        
        # KPIs
        total_monitoring, unique_fields, main_crop = self.data_processor.get_kpi_data()
        
        # Formatar KPIs para exibição
        total_monitoring_str = f"{total_monitoring:,}".replace(',', '.')
        unique_fields_str = f"{unique_fields}"
        
        # Dados para os gráficos
        time_data = self.data_processor.get_time_trend_data()
        field_counts = self.geo_loader.get_field_counts(self.geo_loader.process_geo_data(filtered_df))
        pest_counts = self.data_processor.get_pest_distribution()
        field_analysis = self.data_processor.get_field_analysis()
        crop_severity, severity_col = self.data_processor.get_crop_severity()
        monthly_severity, severity_col_monthly = self.data_processor.get_monthly_severity()
        z_data, x_data, y_data = self.data_processor.get_cooccurrence_data()
        
        # Criar gráficos
        fig_time = TimeSeriesVisualizer.create_time_trend(time_data)
        fig_map = GeographicVisualizer.create_geo_map(field_counts, self.geo_loader.get_geojson())
        fig_pests = DistributionVisualizer.create_pest_distribution(pest_counts)
        fig_fields = DistributionVisualizer.create_field_analysis(field_analysis)
        fig_crop_severity = DistributionVisualizer.create_crop_severity(crop_severity, severity_col)
        fig_severity = TimeSeriesVisualizer.create_severity_analysis(monthly_severity, severity_col_monthly)
        fig_cooccur = CorrelationVisualizer.create_cooccurrence(z_data, x_data, y_data)
        
        return (
            total_monitoring_str,
            unique_fields_str,
            main_crop,
            fig_time,
            fig_map,
            fig_pests,
            fig_fields,
            fig_crop_severity,
            fig_severity,
            fig_cooccur
        )