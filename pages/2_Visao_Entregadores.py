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
from streamlit_folium import folium_static
#----------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------#
#Funções do StreamLit
#----------------------------------------------------------------------------------#
def top_delivers(df1, top_asc):
    df2 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']
        ].groupby(['City','Delivery_person_ID']).max().sort_values(['City','Time_taken(min)'],
        ascending=top_asc).reset_index()

    df_aux01 = df2.loc[df2['City']=='Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City']=='Urban', :].head(10)
    df_aux03 = df2.loc[df2['City']=='Semi-Urban	', :].head(10)
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    
    return df3

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
st.header("Marketplace - Visão Entregadores")

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

#----------------------------------------------------------------------------------#
#Layout no Streamlit 
#----------------------------------------------------------------------------------#

tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "Visão Tática", "Visão Geográfica"])

with tab1:
    with st.container():
        st.title("Overall Metrics")
        col1, col2, col3, col4 = st.columns(4, gap="Large")

        with col1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            st.metric("Maior de idade", maior_idade)

        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            st.metric("Menor de idade", menor_idade)

        with col3:
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            st.metric("Melhor condição", melhor_condicao)

        with col4:
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()        
            st.metric("Pior condição", pior_condicao)


    with st.container():
        st.markdown("""___""")
        st.title("Avaliações")

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Avaliações Médias por Entregador")
            df_avg_ratings_per_deliver = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            df_avg_ratings_per_deliver

        with col2:
            st.subheader("Avaliações Médias por Trânsito")
            df1['Delivery_person_Ratings'] = pd.to_numeric(df1['Delivery_person_Ratings'], errors='coerce')
            df1 = df1.dropna(subset=['Delivery_person_Ratings'])
            df_avg_std_rating_by_traffic = (
                df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                .groupby('Road_traffic_density')
                .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            # Renomeando as colunas
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']
            # Resetando o índice
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            print(df_avg_std_rating_by_traffic)
            st.dataframe(df_avg_std_rating_by_traffic)

            st.subheader("Avaliações Médias por Clima")      
            df1['Delivery_person_Ratings'] = pd.to_numeric(df1['Delivery_person_Ratings'], errors='coerce')
            df1 = df1.dropna(subset=['Delivery_person_Ratings'])
            df_avg_std_rating_by_traffic = (
                df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                .groupby('Weatherconditions')
                .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            # Renomeando as colunas
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']
            # Resetando o índice
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            print(df_avg_std_rating_by_traffic)
            st.dataframe(df_avg_std_rating_by_traffic)


    with st.container():
        st.markdown("""___""")
        st.title("Velocidade de Entrega")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top Entregadores mais Rápidos")
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)

        with col2:
            st.subheader("Top Entregadores mais Lentos")
            df3 = top_delivers(df1, top_asc=False)
            st.dataframe(df3)



