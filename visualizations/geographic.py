"""
Componentes de visualização geográfica
"""
import plotly.express as px
import plotly.graph_objects as go
from config import COLOR_SCHEMES, MAPBOX_STYLE

class GeographicVisualizer:
    """Classe para criar visualizações geográficas"""
    
    @staticmethod
    def create_geo_map(field_counts, campo_geojson=None):
        """
        Cria mapa geográfico com os pontos e limites dos campos
        
        Args:
            field_counts (pandas.DataFrame): DataFrame com contagens por campo
            campo_geojson (dict, optional): GeoJSON com limites dos campos. Defaults to None.
            
        Returns:
            plotly.graph_objects.Figure: Figura do mapa
        """
        if field_counts is None or len(field_counts) == 0:
            fig = go.Figure()
            fig.update_layout(title="Sem dados geográficos para exibir")
            return fig
            
        fig = px.scatter_mapbox(
            field_counts,
            lat='latitude',
            lon='longitude',
            size='count',
            color='count',
            hover_name='loc_name',
            color_continuous_scale=COLOR_SCHEMES['success'],
            size_max=25,
            zoom=3,
            mapbox_style=MAPBOX_STYLE,
            title='Distribuição Geográfica de Monitoramentos'
        )
        
        # Adicionar os limites dos campos como camada de fundo
        if campo_geojson:
            fig.update_layout(
                mapbox={
                    'style': MAPBOX_STYLE,
                    'zoom': 3,
                    'center': {'lat': field_counts['latitude'].mean(), 'lon': field_counts['longitude'].mean()},
                    'layers': [{
                        'source': campo_geojson,
                        'type': "fill",
                        'below': "traces",
                        'color': "rgba(180, 180, 180, 0.4)",   # Cor de preenchimento
                        'opacity': 0.8,                        # Opacidade geral da camada
                        'line': {
                            'width': 1                         # Largura da linha de contorno
                        }
                    }]
                }
            )
            
        return fig