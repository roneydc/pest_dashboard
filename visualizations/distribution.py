"""
Componentes de visualização para gráficos de distribuição
"""
import plotly.express as px
import plotly.graph_objects as go
from config import COLOR_SCHEMES

class DistributionVisualizer:
    """Classe para criar visualizações de distribuição"""
    
    @staticmethod
    def create_pest_distribution(pest_counts):
        """
        Cria gráfico de distribuição de pragas
        
        Args:
            pest_counts (pandas.DataFrame): DataFrame com contagens de pragas
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico
        """
        if pest_counts is None or len(pest_counts) == 0:
            fig = go.Figure()
            fig.update_layout(title="Sem dados de pragas para exibir")
            return fig
            
        fig = px.bar(
            pest_counts,
            x='count',
            y='et_name_pest',
            orientation='h',
            title='Top 10 Tipos de Pragas PT201',
            labels={'count': 'Número de Monitoramentos', 'et_name_pest': 'Tipo de Praga'},
            color='count',
            color_continuous_scale=COLOR_SCHEMES['danger']
        )
        
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        return fig
    
    @staticmethod
    def create_field_analysis(field_analysis):
        """
        Cria gráfico de análise por campo
        
        Args:
            field_analysis (pandas.DataFrame): DataFrame com análise por campo
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico
        """
        if field_analysis is None or len(field_analysis) == 0:
            fig = go.Figure()
            fig.update_layout(title="Sem dados de campos para exibir")
            return fig
            
        fig = px.bar(
            field_analysis,
            x='count',
            y='loc_name',
            orientation='h',
            title='Top 10 Campos com Maior Incidência',
            labels={'count': 'Número de Monitoramentos', 'loc_name': 'Campo'},
            color='count',
            color_continuous_scale=COLOR_SCHEMES['secondary']
        )
        
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        return fig
    
    @staticmethod
    def create_crop_severity(crop_severity, severity_col):
        """
        Cria gráfico de severidade por cultura
        
        Args:
            crop_severity (pandas.DataFrame): DataFrame com severidade por cultura
            severity_col (str): Nome da coluna de severidade
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico
        """
        if crop_severity is None or len(crop_severity) == 0 or severity_col is None:
            fig = go.Figure()
            fig.update_layout(title="Sem dados de severidade disponíveis")
            return fig
            
        fig = px.bar(
            crop_severity,
            x=severity_col,
            y='et_name_crop',
            orientation='h',
            title=f'Top 10 Culturas por Severidade Média ({severity_col})',
            labels={severity_col: f'Severidade Média ({severity_col})', 'et_name_crop': 'Cultura'},
            color=severity_col,
            color_continuous_scale=COLOR_SCHEMES['warning']
        )
        
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        return fig