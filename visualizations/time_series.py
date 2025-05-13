"""
Componentes de visualização para séries temporais
"""
import plotly.express as px
import plotly.graph_objects as go
from config import COLOR_SCHEMES

class TimeSeriesVisualizer:
    """Classe para criar visualizações de séries temporais"""
    
    @staticmethod
    def create_time_trend(time_data):
        """
        Cria gráfico de tendência temporal
        
        Args:
            time_data (pandas.DataFrame): DataFrame com dados temporais
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico
        """
        if time_data is None or len(time_data) == 0:
            fig = go.Figure()
            fig.update_layout(title="Sem dados temporais para exibir")
            return fig
            
        fig = px.line(
            time_data, 
            x='month_year', 
            y='count', 
            title='Tendência de Monitoramentos ao Longo do Tempo',
            labels={'month_year': 'Mês/Ano', 'count': 'Número de Monitoramentos'},
            color_discrete_sequence=[px.colors.qualitative.Safe[0]]
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
        return fig
    
    @staticmethod
    def create_severity_analysis(monthly_severity, severity_col):
        """
        Cria gráfico de análise de severidade mensal
        
        Args:
            monthly_severity (pandas.DataFrame): DataFrame com severidade mensal
            severity_col (str): Nome da coluna de severidade
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico
        """
        if monthly_severity is None or len(monthly_severity) == 0 or severity_col is None:
            fig = go.Figure()
            fig.update_layout(title="Dados insuficientes para análise de severidade mensal")
            return fig
            
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                x=monthly_severity['month_name'],
                y=monthly_severity['mean'],
                name=f'Severidade Média',
                marker_color='royalblue'
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=monthly_severity['month_name'],
                y=monthly_severity['max'],
                name=f'Severidade Máxima',
                mode='lines+markers',
                marker=dict(color='firebrick'),
                line=dict(color='firebrick')
            )
        )
        
        fig.update_layout(
            title=f'Análise de Severidade Mensal ({severity_col})',
            xaxis_title='Mês',
            yaxis_title=f'Severidade ({severity_col})',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig