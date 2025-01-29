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

def top_delivers ( df1, top_asc):
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
              .groupby(['City','Delivery_person_ID'])
              .max()
              .sort_values(['City','Time_taken(min)'], ascending = top_asc).reset_index())

    df_aux01 = df2.loc[df2['City']=='Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City']=='Urban', :].head(10)
    df_aux03 = df2.loc[df2['City']=='Semi-Urban	', :].head(10)
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)

    return df3 
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
#Montagem do Layout no Streamlit - Visão dos Entregadores
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_','_'])
with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap='small')
        with col1:
            #Maior Idade dos Entregadores 👀
            maior_idade = df1.loc[:,'Delivery_person_Age'].max()
            col1.metric('Maior de Idade', maior_idade)

        with col2:
            #Menor Idade dos Entregadores 👀
            menor_idade = df1.loc[:,'Delivery_person_Age'].min()
            col2.metric('Menor de Idade', menor_idade)
    
        with col3:
            # Melhor Condição dos Veículos 👀 
            melhor_condicao = df1.loc[:,'Vehicle_condition'].max()
            col3.metric('Menor Condição do Veículo', melhor_condicao) 

        with col4:
            # Pior Condição dos Veículos 👀
            pior_condicao = df1.loc[:,'Vehicle_condition'].min()
            col4.metric('Pior Condição do Veículo', pior_condicao)
#====================================================================================================

#====================================================================================================
    #Avaliação Média por Entregador
    with st.container():
        st.markdown("""___""")
        st.title('Avaliações')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliação Média por Entregador')
            df_avg_ratings_per_deliver = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                          .groupby('Delivery_person_ID')
                                          .mean().
                                          reset_index())
            st.dataframe(df_avg_ratings_per_deliver)
#====================================================================================================

#====================================================================================================
        with col2:
            #========== Avaliação Média por Trânsito ==========#
            st.markdown ('##### Avaliação Média por Trânsito')
            df1['Delivery_person_Ratings'] = pd.to_numeric(df1['Delivery_person_Ratings'], errors='coerce')
            df1 = df1.dropna(subset=['Delivery_person_Ratings'])

            df_avg_std_rating_by_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                .groupby('Road_traffic_density')
                .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            
            # Renomeando as colunas
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']

            # Resetando o índice
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            st.dataframe(df_avg_std_rating_by_traffic)

            #========== Avaliação Média por Clima ==========#
            st.markdown (' ##### Avaliação Média por Clima')
            df1['Delivery_person_Ratings'] = pd.to_numeric(df1['Delivery_person_Ratings'], errors='coerce')
            df1 = df1.dropna(subset=['Delivery_person_Ratings'])

            df_avg_std_rating_by_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
            .groupby('Weatherconditions')
            .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            # Renomeando as colunas
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']

            # Resetando o índice
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            st.dataframe(df_avg_std_rating_by_traffic)
#====================================================================================================

#====================================================================================================
    with st.container():
        st.markdown("""___""")
        st.title('Velocidade de Entrega')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown ('##### Top Entregadores mais Rápidos')
            df3 = top_delivers ( df1, top_asc=True )
            st.dataframe(df3)   

        with col2:
            st.markdown ('##### Top Entregadores mais Lentos')  
            df3 = top_delivers ( df1, top_asc=False )
            st.dataframe(df3)   
#====================================================================================================


