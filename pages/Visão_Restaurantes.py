#====================================================================================================
#Importação das Bibliotecas
import folium
import streamlit as st
import pandas as pd
import plotly.express as px
from haversine import haversine, Unit
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static
import numpy as np
import plotly.graph_objects as go
#====================================================================================================

#====================================================================================================
#Dataframe e Importação dos dados para aplicação da Análise
df = pd.read_csv('Dataset/train.csv')
df1 = df.copy()
#====================================================================================================

#====================================================================================================
#Funções

def distance(df1):
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
    df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine(
                            (x['Restaurant_latitude'], x['Restaurant_longitude']),
                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1 )
    avg_distance = np.round( df1['distance'].mean(), 2 )
    return avg_distance

def avg_std_time_delivery(df1, festival, op):
    """
    Essa função calcula o tempo médio eo desvio padrão do tempo de entrega.
        Parâmetros:
            Imput:
                - df: Dataframe com os dados necessários para o cálculado
                - op: Tipo de operação que precisa ser cálculado
                    'avg_time': Cálcula o tempo Médio
                    'std_time': Cálcula o desvio padrçao do tempo.
            Output:
                - df: Dataframe com 2 colulas e 1 linha.
                """
    df_aux = (df1.loc [:, ['Time_taken(min)','Festival']]
                 .groupby ('Festival' )
                 .agg ({'Time_taken(min)': ['mean', 'std']}))
                
    df_aux.columns = ['avg_time', 'std_time']                                                     
    df_aux = df_aux.reset_index()

    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2 )
    return df_aux

def avg_std_time_graph (df1):
    df_aux = (df1.loc[:, ['City', 'Time_taken(min)']]
                 .groupby('City')
                 .agg({'Time_taken(min)': ['mean', 'std']}))
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control',
                    x=df_aux['City'],
                    y=df_aux['avg_time'],
                    error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
                
    return fig
#====================================================================================================

#====================================================================================================
#Limpeza dos Dados
def clean_code(df1):
    """ 
    Esta Função tem a responsabilidade de limpar o Dataframe

        Tipos de Limpeza atribuída:
        1. Remoção dos dados NaN
        2. Mudança do tipo de Colunas de Dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de dadas
        5. Limpeza da Coluna de tempo (Remoção do texto da viariável numérica)
    
    Imput:  Dataframe
    Output: Dataframe   
    """
    # 1. Conversão a coluna Age de texto para número
    linhas_selecionadas = (df1 ['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    df1.shape
    linhas_selecionadas = (df1 ['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = (df1 ['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = (df1 ['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # 2. Conversão a coluna de Ratings de texto para número decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # 3. Conversão da coluna order_date de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

    # 4. Conversão de Multiple_deliveries para Interiro
    linhas_selecionadas = (df1 ['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    # 5. Removendo os espaços dentro de strings/texto/objects
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # 6. Limpeza sobre a coluna Time_taken(min)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ' )[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

    return df1
df1 = clean_code(df)
#====================================================================================================

#====================================================================================================
#Aba de comamando no Streamlit - Comando Lateral

st.header('Marketplace - Visão de Clientes')

image_path = 'Logo.png' 
image = Image.open(image_path)  
st.sidebar.image(image, width=300)

st.sidebar.markdown ( '# Curry Company' )
st.sidebar.markdown ( '## Fastest Delivery in Town' )
st.sidebar.markdown ( """___""") 

st.sidebar.markdown ( '## Selecione uma data Limite'  )

date_slider = st.sidebar.slider('Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')
st.sidebar.markdown ( """___""") 

traffic_options = st.sidebar.multiselect('Quais as condições do Trânsito',
    ['low', 'Medium', 'High', 'Jam'],
    default=['low', 'Medium', 'High', 'Jam'])

# Usar a data selecionada no slider
st.write(f"Data selecionada: {date_slider.strftime('%d-%m-%Y')}")

linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

linhas_selecionadas = df1['Road_traffic_density'].isin (traffic_options)
st.dataframe(df1)
#====================================================================================================

#====================================================================================================
tab1, tab2, tab3, =st.tabs(['Visão dos Restaurantes','_','_'])
with tab1:
    with st.container():
        st.title('Overal Metrics')

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1: 
            delivery_unique =  len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregadores Únicos', delivery_unique)

        with col2:
            avg_distance = distance (df1)
            col2.metric('Distância Média', avg_distance)

        with col3:
            df_aux = avg_std_time_delivery ( df1, 'Yes', 'avg_time' )
            col3.metric('Entregas no Festival', df_aux)
                
        with col4:
            df_aux = avg_std_time_delivery ( df1, 'Yes', 'std_time' )
            col4.metric('Desvio Padrão Médio', df_aux)

        with col5:
            df_aux = avg_std_time_delivery ( df1, 'No', 'std_time' )
            col5.metric('Tempo Médio de Entrega c/Festival', df_aux)
   
        with col6:
            df_aux = avg_std_time_delivery ( df1, 'No', 'std_time' )
            col6.metric('Desvio Padrão Médio', df_aux)

#====================================================================================================

#====================================================================================================
    with st.container():
        st.markdown('''___''')
        st.title('Tempo Médio de Entrega por Cidade')

        col1, col2 = st.columns(2)
        with col1:
            fig = avg_std_time_graph( df1 ) 
            st.plotly_chart( fig )

        with col2:
            df_aux = (df1.loc [:, ['City', 'Time_taken(min)','Type_of_order']]
            .groupby (['City','Type_of_order'] )
            .agg ({'Time_taken(min)': ['mean', 'std']}))
            
            df_aux.columns = ['avg_time', 'std_time']                                                     
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)
#====================================================================================================

#====================================================================================================
    with st.container():
        st.markdown('''___''')
    
    col1, col2 = st.columns(2)

    with col1:
        df1['distance'] = df1.loc[:, ['Delivery_location_latitude', 'Delivery_location_longitude',
                'Restaurant_latitude', 'Restaurant_longitude']].apply(lambda x: haversine(
                        (x['Restaurant_latitude'], x['Restaurant_longitude']),
                        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])),
                        axis=1 )

        avg_distance = df1.loc[:,[ 'City', 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure ( data = 
                 [go.Pie ( labels = avg_distance ['City'], 
                          values=avg_distance ['distance'], 
                          pull = [0.01, 0.01, 0.01])])
        st.plotly_chart(fig)
    
    with col2:
        df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                 .groupby(['City', 'Road_traffic_density'])
                 .agg({'Time_taken(min)': ['mean', 'std']}))
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()

        fig = px.sunburst(df_aux, 
                            path=['City', 'Road_traffic_density'], 
                            values='avg_time',
                            color='std_time', 
                            color_continuous_scale='RdBu',
                            color_continuous_midpoint=np.average(df_aux['std_time']))
        st.plotly_chart(fig)
#====================================================================================================