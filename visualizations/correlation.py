"""
Componentes de visualização para gráficos de correlação
"""
import plotly.express as px
import plotly.graph_objects as go
from config import COLOR_SCHEMES

class CorrelationVisualizer:
    """Classe para criar visualizações de correlação"""
    
    @staticmethod
    def create_cooccurrence(z_data, x_data, y_data):
        """
        Cria matriz de co-ocorrência
        
        Args:
            z_data (numpy.ndarray): Dados para o heatmap
            x_data (list): Lista de labels para o eixo X
            y_data (list): Lista de labels para o eixo Y
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico
        """
        if z_data is None or x_data is None or y_data is None:
            fig = go.Figure()
            fig.update_layout(title="Dados insuficientes para matriz de co-ocorrência")
            return fig
            
        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=x_data,
            y=y_data,
            colorscale=COLOR_SCHEMES['info'],
            hoverongaps=False,
            colorbar=dict(title='Número de<br>Monitoramentos')
        ))
        
        fig.update_layout(
            title='Co-ocorrência entre Pragas e Culturas (Top 6 de Cada)',
            xaxis_title='Cultura',
            yaxis_title='Tipo de Praga',
            xaxis_tickangle=-45
        )
        
        return fig