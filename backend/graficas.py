
import plotly.express as px

def crear_grafico_pie(dataframe, viven_espana=True):
    # Filtro para el DataFrame
    filtro = dataframe['vives_espana'] == viven_espana
    df_filtrado = dataframe[filtro]
    
    # Conteo de orientaciones
    colectivos_count = df_filtrado['orientacion'].value_counts().reset_index()
    colectivos_count.columns = ['Orientacion', 'Cantidad']
    
    # Tener en cuenta ambas posibilidades
    titulo = "Distribución de Orientación Sexual"
    if viven_espana:
        titulo += " (Personas que Viven en España)"
    else:
        titulo += " (Personas que No Viven en España)"
    
    # Crear gráfico de pastel
    fig = px.pie(colectivos_count, 
                 values='Cantidad', 
                 names='Orientacion', 
                 title=titulo,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    return fig



def barras_apiladas_genero_orientacion(dataframe):
    # Agrupar y contar las combinaciones de género y orientación
    datos_agrupados = dataframe.groupby(['genero', 'orientacion']).size().reset_index(name='Cantidad')

    # Configurar el gráfico de barras apiladas
    fig = px.bar(datos_agrupados,
                 x='genero',
                 y='Cantidad',
                 color='orientacion',
                 title='Distribución de Género y Orientación Sexual',
                 labels={'genero': 'Género', 'orientacion': 'Orientación Sexual'},
                 barmode='stack',  
                 color_discrete_sequence=px.colors.qualitative.Pastel)

    return fig

def graficar_permiso_residencia(dataframe):
    # Contar las frecuencias de los valores en la columna 'permiso_residencia'
    permiso_count = dataframe['permiso_residencia'].value_counts().reset_index()
    permiso_count.columns = ['Permiso de Residencia', 'Cantidad']
    
    # Calcular los porcentajes
    total = permiso_count['Cantidad'].sum()
    permiso_count['Porcentaje'] = (permiso_count['Cantidad'] / total) * 100
    
    # Calcular el índice de la sección con el valor más grande
    max_value_index = permiso_count['Cantidad'].idxmax()
    
    # Crear un vector donde la porción con el valor más grande será destacada
    pull_values = [0 if i != max_value_index else 0.1 for i in range(len(permiso_count))]
    
    # Crear gráfico de pastel (pie chart) con cantidades y porcentajes
    fig = px.pie(permiso_count, 
                 names='Permiso de Residencia', 
                 values='Cantidad', 
                 title='Distribución de Permisos de Residencia',
                 labels={'Permiso de Residencia': 'Tipo de Permiso'},
                 color='Permiso de Residencia',
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 hole=0.3)  # Pie chart con un agujero en el centro (tipo donut)
    
    # Añadir texto de porcentajes y cantidades dentro del gráfico
    fig.update_traces(pull=pull_values)
    
    return fig


def graficar_combinaciones(dataframe):
    # Agrupación y conteo
    combinaciones = dataframe.groupby(['persona_racializada', 'discapacitade', 'sin_hogar', 'migrante']).size().reset_index(name='Cantidad')
    
    # Crear una nueva columna que combine las condiciones
    combinaciones['Combinación'] = combinaciones.apply(
        lambda row: f"Racializada: {row['persona_racializada']}, Discapacidad: {row['discapacitade']}, "
                    f"Hogar: {row['sin_hogar']}, Migrante: {row['migrante']}", axis=1)
    
    # Configuración gráfico de barras
    fig = px.bar(combinaciones, 
                 x='Combinación', 
                 y='Cantidad', 
                 title='Frecuencia de Combinaciones de Condiciones',
                 labels={'Combinación': 'Combinación de Condiciones', 'Cantidad': 'Número de Personas'},
                 color='Cantidad',
                 color_continuous_scale='Viridis')

    # Etiquetas en el gráfico
    fig.update_layout(xaxis_tickangle=45)
    
    return fig