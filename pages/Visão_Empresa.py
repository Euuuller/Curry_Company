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
#====================================================================================================

#====================================================================================================
#Dataframe e Importação dos dados para aplicação da Análise
df = pd.read_csv('Dataset/train.csv')
df1 = df.copy()
#====================================================================================================

#====================================================================================================
#Funções
def order_metric( df1 ):
    #Order Metric
    cols = ['ID', 'Order_Date']
    #Seleção de Linhas
    df_aux = df1.loc[:, cols].groupby( 'Order_Date' ).count().reset_index()
    # Desenho do Gráfico de Barras para representar
    fig = px.bar ( df_aux, x='Order_Date', y='ID')
    return fig

def traffic_order_share(df1):
    df_aux = (df1.loc[:, ['ID', 'Road_traffic_density']]
                 .groupby('Road_traffic_density')
                 .count()
                 .reset_index())
            
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, values='ID', names='Road_traffic_density')
    return fig

def traffic_order_city (df1):
            df_aux = (df1.loc[:,['ID', 'City', 'Road_traffic_density']]
                        .groupby(['City', 'Road_traffic_density'])
                        .count()
                        .reset_index())
        
            fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
            return fig  

def order_by_week(df1):
    df1 ['week_of_year']  = ( df1 ['Order_Date']
                            .dt.strftime( '%U' ))
    df_aux = ( df1.loc[:, ['ID', 'week_of_year']]
                            .groupby( 'week_of_year' )
                            .count()
                            .reset_index())
    fig = px.line(df_aux, x='week_of_year', y='ID')

    return fig

def order_share_by_week(df1):
    df_aux01 = ( df1.loc[:, ['ID', 'week_of_year']]
                    .groupby('week_of_year')
                    .count()
                    .reset_index())

    df_aux02 = ( df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                    .groupby('week_of_year')
                    .nunique()
                    .reset_index())
    df_aux = pd.merge(df_aux01, df_aux02, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
            
    return fig

def country_maps(df1):        
    df_aux = ( df.loc[:, ['City','Road_traffic_density',
    'Delivery_location_latitude', 'Delivery_location_longitude']]
                 .groupby(['City', 'Road_traffic_density'])
                 .median()
                 .reset_index()) 
    df_aux.dropna(subset=['City', 'Road_traffic_density'], inplace=True)
    df_aux = df_aux.head(30)
    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info ['Delivery_location_latitude'],
        location_info ['Delivery_location_longitude']],
        popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
        
    folium_static (map, width=1024, height=600)
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
#Montagem do Layout no Streamlit
tab1, tab2, tab3 = st.tabs (['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

# 1. Quantidade de Pedidos por dia. 🔰
with tab1:
    
    with st.container():
        fig = order_metric( df1 )
        st.header('Order by Day')
        st.plotly_chart(fig, use_container_width=True)
#====================================================================================================  
        
#====================================================================================================   
with tab1:
    with st.container():
        col1, col2 = st.columns(2)
    
    # 3. Distribuição por pedidos por tipo de tráfego. 🔰
    with col1:
        st.header('Traffic Order Share')
        fig = traffic_order_share( df1 )
        st.plotly_chart(fig, use_container_width=True)

    # 4. Comparação do Volume de pedidos por cidade e tipo de tráfego. 🔰
    with col2:
        st.header('Traffic Order City')
        fig = traffic_order_city ( df1 )
        st.plotly_chart(fig, use_container_width=True)
#====================================================================================================

#====================================================================================================
with tab2:
    with st.container():
        st.markdown('# Order by Week')
        fig = order_by_week (df1)
        st.plotly_chart(fig, use_container_width=True)    

    with st.container():
        st.markdown('# week of Year')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
#====================================================================================================

#====================================================================================================
with tab3:
    st.markdown( '# Contry maps' )
    country_maps(df1)
#====================================================================================================

