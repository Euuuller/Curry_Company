#----------------------------------------------------------------------------------#
#Importação de Bibliotecas
#----------------------------------------------------------------------------------#
from haversine import haversine
from datetime import datetime
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import folium_static
#----------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
#Funções do StreamLit
#----------------------------------------------------------------------------------#
def distance(df1, fig):
    if fig == False:
        col2 = ["Delivery_location_latitude", 'Delivery_location_longitude', 
                'Restaurant_latitude', 'Restaurant_longitude']
        # Calculando a distância
        df1['distance'] = df1.loc[:, col2].apply(lambda x: haversine(
            (x['Restaurant_latitude'], x['Restaurant_longitude']),
            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
        ), axis=1)
        avg_distance = df1['distance'].mean()
        return avg_distance
    else:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine(
                                                    (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
            fig = go.Figure(data=[go.Pie(
                labels=avg_distance['City'], 
                values=avg_distance['distance'], 
                pull=[0.01, 0.01, 0.01],
                marker=dict(colors=['#FF0000', '#00FF00', '#0000FF'])  # Vermelho, Verde, Azul
                )])
            return fig


def avg_std_time_delivery(df1, festival, op):
    """
    Esta função calcula o tempo médio e o desvio padrão do tempo de entrega.
    Parâmetros:
        Imput:
            - df: Dataframe com os dados necessários para o cálculo.
            - op: Tipo de operação (entrega ou coleta).
                "avg_time": Tempo médio de entrega.
                "std_time": Desvio padrão do tempo de entrega.
        Output:
            - df_aux: Dataframe com os resultados do cálculo, 2 colunas e 1 linha.
    """       
    df_aux = (df1.loc [:, ['Time_taken(min)','Festival']].groupby 
            (['Festival'] ).agg ({'Time_taken(min)': ['mean', 'std']}))
    df_aux.columns = ['avg_time', 'std_time']                                                     
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2)

    return df_aux


def avg_std_time_graph(df1):
    cols = ['City', 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control',
                                x=df_aux['City'],
                                y=df_aux['avg_time'],
                                error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
    return fig

def avg_std_time_on_traffic(df1):    
    cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, 
                    path=['City', 'Road_traffic_density'], 
                    values='avg_time',
                    color='std_time', 
                    color_continuous_scale='RdBu',
                    color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig




#----------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
# Import Dataset
#----------------------------------------------------------------------------------#
df = pd.read_csv('Dataset/train.csv')
df1 = df.copy()
#----------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
# Funções de Limpeza de Dados
#----------------------------------------------------------------------------------#
def clean_code(df1):
    """
    Esta função realiza a limpeza de dados do DataFrame df1.
    Tipos de limpeza realizados:
        1. Conversão da coluna 'Delivery_person_Age' de texto para número inteiro.
        2. Conversão da coluna 'Delivery_person_Ratings' de texto para número decimal (float).
        3. Conversão da coluna 'Order_Date' de texto para data.
        4. Conversão da coluna 'multiple_deliveries' de texto para número inteiro.
        5. Remoção de espaços em branco dentro de strings/texto/objects.
        6. Limpeza da coluna 'Time_taken(min)' para manter apenas o valor numérico.
    
    Parâmetros:
        df1 (pandas.DataFrame): DataFrame a ser limpo.
    
    Retorna:
        pandas.DataFrame: DataFrame limpo.
    """
#----------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
# 1. Conversão a coluna Age de texto para número
linhas_selecionadas = (df1 ['Delivery_person_Age'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['Delivery_person_Age'] = df1['Delivery_person_Age']. astype( int )
df1.shape

linhas_selecionadas = (df1 ['Road_traffic_density'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1 ['City'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1 ['Festival'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()


# 2. Conversão a coluna de Ratings de texto para número decimal (float)
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings']. astype( float )

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
#----------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
#Barra Lateral do StreamLit
#----------------------------------------------------------------------------------#
st.header("Marketplace - Visão Restaurantes")

# Carregar imagem
image_path = "Logo.png"
image = Image.open('Logo.png')
st.sidebar.image(image, width=300)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""___""")
st.sidebar.markdown("## Selecione uma data limite")

# Armazenar o valor do slider em uma variável
data_limite = st.sidebar.slider(
    "Até qual data?",
    value=datetime(2022, 4, 6),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format="MM-DD-YYYY")

st.sidebar.markdown("""___""")
traffic_options = st.sidebar.multiselect(
    "Quais as Condições de Trânsito",
    ["Low", "Medium", "High", "Jam"], 
    default=["Low", "Medium", "High", "Jam"])
st.sidebar.markdown("""___""")
st.sidebar.markdown("## Powered by Comunidade DS")

# Filtros (assumindo que a coluna de data se chama 'Order_Date' - ajuste conforme seu DataFrame)
if 'Order_Date' in df1.columns:
    linhas_selecionadas = df1["Order_Date"] < data_limite
    df1 = df1.loc[linhas_selecionadas, :]
else:
    st.warning("Coluna de data não encontrada no DataFrame")

# Filtro de tráfego
linhas_selecionadas = df1["Road_traffic_density"].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

st.dataframe(df1)


#----------------------------------------------------------------------------------#
#Layout no Streamlit 
#----------------------------------------------------------------------------------#

tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "-", "-"])

with tab1:
    with st.container():
        st.title("Overal Metrics")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            delivery_unique =  len(df1.loc[:, 'Delivery_person_ID'].unique())
            st.metric("Entregadores Únicos", delivery_unique)
 
        with col2:
            avg_distance = distance(df1, fig = False)
            st.metric("Distância Média das Entregas", f"{avg_distance:.2f} KM")

        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time')
            col3.metric("Tempo Médio de Entrega c/ Festival", df_aux)

        with col4:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'std_time')
            col4.metric("Desvio Padrão Médio de Entrega c/ Festival", df_aux)

        with col5:
            df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
            col5.metric("Tempo Médio de Entrega c/ Festival", df_aux)
                
        with col6:
            df_aux = avg_std_time_delivery(df1, 'No', 'std_time')
            col6.metric("Desvio Padrão Médio de Entrega c/ Festival", df_aux)

    with st.container():
        st.markdown("""___""")
        col1, col2  = st.columns(2)

        with col1:
            fig = avg_std_time_graph(df1)
            st.plotly_chart(fig)


        with col2:
            cols = ['City', 'Time_taken(min)','Type_of_order']
            df_aux = df1.loc [:, cols].groupby (['City','Type_of_order'] ).agg ({'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']                                                     
            df_aux = df_aux.reset_index()
            df_aux

    with st.container():
        col1, col2  = st.columns(2)

        with col1:
            fig = distance(df1, fig=True)
            st.plotly_chart(fig)

        with col2:
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart(fig)