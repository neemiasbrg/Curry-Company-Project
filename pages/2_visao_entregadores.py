import pandas as pd
import re
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image
import folium
import datetime

st.set_page_config( page_title='Visão Entregadores' , page_icon=r"C:\Users\Neemias G Braga\Music\node_modules\serve-index\public\icons\map.png" , layout='wide' )

#===================================================
#Funções
#===================================================
def top_delivers (df1, top_asc):

    df2 = df_filtered.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)' ]].groupby( ['City', 'Delivery_person_ID'] ).max().sort_values(['City', 'Time_taken(min)'], ascending=top_asc ).reset_index()

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df_aux = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)

    return df1

def clean_code (df1):
    """Esta função é responsável pela limpeza do dataframe

       Tipos de Limpezas:
    
       1. Remoção dos dados NaN
       2. Mudança do tipo da coluna de dados
       3. Remoção dos espaços das variáveis de texto
       4. Fotmatação da coluna de datas
       5. Limpeza da coluna tempo (remoção do texto da variáve numérica)

       Imput: Dataframe
       Output Dataframe
    
    """
    # Remover spaco da string
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

    # Excluir as linhas com a idade dos entregadores vazia
    # ( Conceitos de seleção condicional )
    # Use pd.isna() to check for NaN values more reliably
    linhas_vazias = ~pd.isna(df1['Delivery_person_Age'])
    df1 = df1.loc[linhas_vazias, :]

    # Conversao de texto/categoria/string para numeros inteiros
    # Use pd.to_numeric() with errors='coerce' to handle non-convertible values
    df1['Delivery_person_Age'] = pd.to_numeric(df1['Delivery_person_Age'], errors='coerce').astype('Int64') # Use Int64 to allow for nullable integers

    # Conversao de texto/categoria/strings para numeros decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # Conversao de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )
    # Removendo espaços vazios
    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )
    linhas_vazias = df1['City'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]
    linhas_vazias = df1['Weatherconditions'] != 'conditions NaN'
    df1 = df1.loc[linhas_vazias, :]
    linhas_vazias = df1['Road_traffic_density'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]
    linhas_vazias = df1['Festival'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]

    # Comando para remover o texto de números
    df1 = df1.reset_index( drop=True )
    # Apply re.findall() to each element in the Series
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: re.findall(r'\d+', x)[0] if re.findall(r'\d+', x) else None)
    # Convert the extracted numbers to integers
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype('Int64')

    return df1

#===================================================
#Carregar os dados
#===================================================

df = pd.read_csv('train.csv')

# Criar uma cópia do DataFrame original
df1 = df.copy()

#===================================================
#Limpeza dos dados
#===================================================

df1 = clean_code(df)

#===================================================
#Barra Lateral
#===================================================

st.header('Marketplace - Visão Entregadores')

# Carregar e mostrar a imagem do logo
image_path = 'logo.png'
image = Image.open(image_path)
st.image(image, width=120)

st.sidebar.markdown('### Cury Company')
st.sidebar.markdown('# Fastest Delivery in Town')
st.sidebar.markdown( """---""" )

min_date = df1['Order_Date'].min()
max_date = df1['Order_Date'].max()

# Convert datetime to days since epoch
min_days = int((min_date - pd.Timestamp("1970-01-01")).days)
max_days = int((max_date - pd.Timestamp("1970-01-01")).days)

# Slider na barra lateral para seleção de data
data_slider_days = st.sidebar.slider(
    'Selecione uma data',
    min_value=min_days,
    max_value=max_days,
    value=max_days
)

# Convert days back to datetime
data_slider = pd.Timestamp("1970-01-01") + pd.Timedelta(days=data_slider_days)

st.header(data_slider.strftime('%d-%m-%Y'))
st.sidebar.markdown( """---""" )

traffic_options = st.sidebar.multiselect(
    'Quais as condições de trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default='Low'
)

st.sidebar.markdown( """---""" )

conditions_options = st.sidebar.multiselect(
    'Quais as condições climáticas?',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default='conditions Stormy'
)

st.sidebar.markdown( """---""" )
st.sidebar.markdown('### Powered by Comunidade DS')

# Filtrar dados com base na seleção do slider
df_filtered = df1[(df1['Order_Date'] < data_slider) &
                  (df1['Road_traffic_density'].isin(traffic_options)) &
                  (df1['Weatherconditions'].isin(conditions_options))]

#===================================================
#Layout no Streamlit
#===================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Metricas Gerais')

        col1, col2, col3, col4 = st.columns(4, gap='large')

        with col1:
            #A maior idade dos entregadores.
            maior_idade = df_filtered['Delivery_person_Age'].max()
            col1.metric('A maior idade é', maior_idade)
        with col2:
            #A menor idade dos entregadores.
            menor_idade = df_filtered['Delivery_person_Age'].min()
            col2.metric('A menor idade é:', menor_idade)

        with col3:
            #A pior e a melhor condição de veículos.
            melhor_condicao = df_filtered['Vehicle_condition'].max()
            col3.metric('A melhor condição é:', melhor_condicao)
        with col4:
            #A pior e a melhor condição de veículos.
            pior_condicao = df_filtered['Vehicle_condition'].min()
            col4.metric('A pior condição é:', pior_condicao)

    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')

        col1, col2 = st.columns(2)

        with col1:
            #A avaliação média por entregador
            st.subheader('Avaliações médias por entregador')
            avaliacao_media_entregador = (df_filtered.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']]
                                          .groupby( 'Delivery_person_ID' )
                                          .mean()
                                          .reset_index())
            st.dataframe(avaliacao_media_entregador)
        
        with col2:
            #A avaliação média e o desvio padrão por tipo de tráfego.
            st.subheader('Avaliação média por trânsito')
            df_filtered.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby( 'Road_traffic_density' ).describe()
            df_aux = (df_filtered.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                      .groupby( 'Road_traffic_density' )
                      .describe()
                      .reset_index())
            df_aux.columns = ['Road_traffic_density', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
            st.dataframe( df_aux )

            #A avaliação média e o desvio padrão por condições climáticas.
            st.subheader('Avaliação média por clima')
            df_filtered.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby( 'Weatherconditions' ).describe()
            df_aux = (df_filtered.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                      .groupby( 'Weatherconditions' )
                      .describe()
                      .reset_index())
            df_aux.columns = ['Weatherconditions', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
            st.dataframe( df_aux )

    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')

        col1, col2 = st.columns(2)

        with col1:
            #Os 10 entregadores mais rápidos por cidade.
            st.markdown('##### Top entregadores mais rápidos')
            df_aux = top_delivers(df1, top_asc=True)
            st.dataframe( df_aux )
            
        with col2:
            #Os 10 entregadores mais lentos por cidade.
            st.markdown('##### Top entregadores mais lentos')
            df_aux = top_delivers(df1, top_asc=False)
            st.dataframe( df_aux )