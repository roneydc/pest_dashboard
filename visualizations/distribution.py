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
        Cria gráfico de distribuição de pragas agrupado por código
        
        Args:
            pest_counts (pandas.DataFrame): DataFrame com contagens de pragas por tipo básico
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico
        """
        if pest_counts is None or len(pest_counts) == 0:
            fig = go.Figure()
            fig.update_layout(title="Sem dados de pragas para exibir")
            return fig

        # Verificar se temos o formato esperado com praga_base e count
        if 'praga_base' in pest_counts.columns and 'count' in pest_counts.columns:
            # Determinar se temos informações de código
            has_code_info = 'codigos' in pest_counts.columns and 'num_codes' in pest_counts.columns
            
            # Preparar hover_data
            hover_data = ['count', 'percentage']
            if has_code_info:
                hover_data.extend(['num_codes', 'codigos'])
            
            # Criar hover template personalizado
            if has_code_info:
                hovertemplate = (
                    "<b>%{y}</b><br>" +
                    "Registros: %{x}<br>" +
                    "Porcentagem: %{customdata[0]}%<br>" +
                    "Códigos associados (%{customdata[1]}): %{customdata[2]}<extra></extra>"
                )
                # Preparar dados customizados para hover
                custom_data = list(zip(
                    pest_counts['percentage'], 
                    pest_counts['num_codes'],
                    pest_counts['codigos']
                ))
            else:
                hovertemplate = (
                    "<b>%{y}</b><br>" +
                    "Registros: %{x}<br>" +
                    "Porcentagem: %{customdata[0]}%<extra></extra>"
                )
                # Preparar dados customizados para hover
                custom_data = list(zip(pest_counts['percentage']))
            
            # Criar gráfico de barras
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=pest_counts['count'],
                y=pest_counts['praga_base'],
                orientation='h',
                marker=dict(
                    color=pest_counts['count'],
                    colorscale='Viridis',
                    colorbar=dict(title='Contagem')
                ),
                hovertemplate=hovertemplate,
                customdata=custom_data,
                name=''
            ))
            
            # Adicionar rótulos de porcentagem nas barras
            for i, row in enumerate(pest_counts.itertuples()):
                fig.add_annotation(
                    x=row.count,
                    y=row.praga_base,
                    text=f"{row.percentage:.1f}%",
                    showarrow=False,
                    xshift=10,
                    font=dict(color="black", size=10),
                    xanchor="left"
                )
            
            # Configurar layout
            fig.update_layout(
                title='Distribuição por Tipo Básico de Praga',
                xaxis_title='Número de Monitoramentos',
                yaxis_title='Tipo de Praga',
                yaxis={'categoryorder': 'total ascending'},
                barmode='stack',
                bargap=0.3,
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='white'
            )
            
            # Adicionar grid
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
        else:
            # Versão de fallback
            fig = px.bar(
                pest_counts,
                x='count',
                y='et_name_pest' if 'et_name_pest' in pest_counts.columns else pest_counts.columns[0],
                orientation='h',
                title='Top 10 Tipos de Pragas',
                labels={'count': 'Número de Monitoramentos', 'et_name_pest': 'Tipo de Praga'},
                color='count',
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})

        return fig

    @staticmethod
    def create_field_analysis(field_analysis):
        """
        Cria gráfico de análise por campo com informação de praga dominante
        
        Args:
            field_analysis (pandas.DataFrame): DataFrame com análise por campo e pragas
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico
        """
        if field_analysis is None or len(field_analysis) == 0:
            fig = go.Figure()
            fig.update_layout(title="Sem dados de campos para exibir")
            return fig
            
        # Verificar se temos as colunas necessárias para a versão detalhada
        if 'total' in field_analysis.columns and 'et_code_pest' in field_analysis.columns:
            # Adicionar a coluna field_with_pest se não existir
            if 'field_with_pest' not in field_analysis.columns:
                field_analysis['field_with_pest'] = field_analysis['loc_name'] + ' (' + field_analysis['et_code_pest'] + ')'
            
            # Versão com detalhes da praga dominante
            fig = px.bar(
                field_analysis,
                x='total',
                y='loc_name',
                orientation='h',
                title='Top 10 Campos com Maior Incidência (com Praga Principal)',
                labels={'total': 'Número Total de Monitoramentos', 'loc_name': 'Campo'},
                color='et_code_pest',  # Colorir por código de praga dominante
                hover_name='loc_name',
                hover_data=['total', 'et_code_pest'],
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            # Adicionar uma segunda barra para a praga principal se tivermos os dados
            if 'top_pest_count' in field_analysis.columns:
                fig.add_trace(
                    go.Bar(
                        x=field_analysis['top_pest_count'],
                        y=field_analysis['loc_name'],
                        name='Praga Principal',
                        orientation='h',
                        marker_color='rgba(255, 255, 255, 0.6)',
                        hoverinfo='none',
                        opacity=0.6
                    )
                )
            
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                barmode='overlay',
                legend_title_text='Código da Praga Dominante'
            )
        else:
            # Versão simples para compatibilidade
            fig = px.bar(
                field_analysis,
                x='count',
                y='loc_name',
                orientation='h',
                title='Top 10 Campos com Maior Incidência',
                labels={'count': 'Número de Monitoramentos', 'loc_name': 'Campo'},
                color='count',
                color_continuous_scale='Greens'
            )
            
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        return fig

    @staticmethod
    def create_crop_severity(crop_severity, severity_col):
        """
        Cria gráfico de severidade por cultura e código de praga
        
        Args:
            crop_severity (pandas.DataFrame): DataFrame com severidade por cultura e praga
            severity_col (str): Nome da coluna de severidade
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico
        """
        if crop_severity is None or len(crop_severity) == 0 or severity_col is None:
            fig = go.Figure()
            fig.update_layout(title="Sem dados de severidade disponíveis")
            return fig
        
        # Verificar se temos o formato detalhado com pragas
        if 'et_code_pest' in crop_severity.columns and 'mean_severity' in crop_severity.columns:
            # Verificar/criar a coluna crop_with_pest se não existir
            if 'crop_with_pest' not in crop_severity.columns:
                crop_severity['crop_with_pest'] = crop_severity['et_name_crop'] + ' (' + crop_severity['et_code_pest'] + ')'
            
            # Versão detalhada por praga
            fig = px.bar(
                crop_severity,
                x='mean_severity',
                y='crop_with_pest',  # Usando coluna combinada cultura (código)
                orientation='h',
                title=f'Top 10 Combinações Cultura-Praga por Severidade Média ({severity_col})',
                labels={
                    'mean_severity': f'Severidade Média ({severity_col})', 
                    'crop_with_pest': 'Cultura (Praga)',
                    'count': 'Registros'
                },
                color='et_code_pest',  # Colorir por código de praga
                hover_data=['et_name_crop', 'count'],
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            # Adicionar texto de contagem nas barras se tivermos a coluna
            if 'count' in crop_severity.columns:
                fig.update_traces(text=crop_severity['count'], textposition='outside')
            
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                legend_title_text='Código da Praga'
            )
        else:
            # Versão simples por cultura
            fig = px.bar(
                crop_severity,
                x=severity_col,
                y='et_name_crop',
                orientation='h',
                title=f'Top 10 Culturas por Severidade Média ({severity_col})',
                labels={severity_col: f'Severidade Média ({severity_col})', 'et_name_crop': 'Cultura'},
                color=severity_col,
                color_continuous_scale='Oranges'
            )
            
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        return fig