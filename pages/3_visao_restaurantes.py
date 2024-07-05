import pandas as pd
import numpy as np
import re
from haversine import haversine, Unit

import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image
import folium
import datetime

st.set_page_config( page_title='Visão Restaurantes' , page_icon=r"C:\Users\Neemias G Braga\Music\node_modules\serve-index\public\icons\map.png" , layout='wide' )

#===================================================
#Funções
#===================================================
def avg_std_time_on_traffic (df1):

            colunas = ['City', 'Time_taken(min)']

            df1_aux = df1.groupby('City').agg({'Time_taken(min)': ['mean', 'std']})

            df1_aux.columns = ['avg_time', 'std_time']

            df1_aux = df1_aux.reset_index()

            fig = px.sunburst(df1_aux, path=['City'], values='avg_time', color='std_time', color_continuous_scale='RdBu',
                              color_continuous_midpoint=np.average(df1_aux['std_time']))
            
            return fig

def avg_std_time_graph (df1):

    colunas = ['City','Time_taken(min)']

    df1_aux = df1.loc[:, colunas].groupby( 'City' ).agg({'Time_taken(min)': ['mean','std']})

    df1_aux.columns = ['avg_time','std_time']

    df1_aux = df1_aux.reset_index()

    fig = go.Figure()
    fig.add_trace( go.Bar( name='control', x=df1_aux['City'], y=df1_aux['avg_time'], error_y=dict(type='data', array=df1_aux['std_time'])))
    fig.update_layout(barmode='group')


    return fig


def avg_std_time_delivery(df1, festival, op):
                """Esta função calcula o tempo médio e o desvio padrão do tempo de entrega
                   Parâmetros:
                        Imput:
                           - df: Dataframe com os dados necessários para o cálculo
                           - op: Tipo de operação que precisa ser calculada
                                'avg_time': Calcula o tempo médio
                                'std_time': Calcula o desvio padrão do tempo.
                        Output:
                            - df: Dataframe com duas colunas e 1 linha        
                """
         
                df1_aux = (df1.loc[:, ['Time_taken(min)','Festival']].groupby( 'Festival' )
                                                                .agg({'Time_taken(min)': ['mean','std']}))

                df1_aux.columns = ['avg_time','std_time']

                df1_aux = df1_aux.reset_index()

                return df1_aux[op]
 

def distancia (df1):

   colunas = ['Restaurant_latitude' , 'Restaurant_longitude', 'Delivery_location_latitude' , 'Delivery_location_longitude']

   df1['distancia'] = df1.loc[:, colunas].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

   distancia_media = np.round(df1['distancia'].mean(), 2)
            

   return distancia_media

def clean_code (df1):
    """Esta função é responsável pela limpeza do dataframe

       Tipos de Limpezas:
    
       1. Remoção dos dados NaN
       2. Mudança do tipo da coluna de dados
       3. Remoção dos espaços das variáveis de texto
       4. Formatação da coluna de datas
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

st.header('Marketplace - Visão Restaurantes')

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
    default=['Low']
)

st.sidebar.markdown( """---""" )

conditions_options = st.sidebar.multiselect(
    'Quais as condições climáticas?',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default=['conditions Stormy']
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
# Layout no Streamlit
tab1, tab2, tab3 = st.columns([3, 1, 1])
tab1.header('Visão Gerencial')
tab2.header('')
tab3.header('')

with tab1:

    st.title('Métricas Gerais')

    with st.container():
        

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            entregadores_unicos = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregadores Únicos', entregadores_unicos)

        with col2:
            distancia_media = distancia(df1)
            col2.metric('Distância média dos entregadores e locais de entrega:', distancia_media)
           
        with col3:
            df1_aux = avg_std_time_delivery (df1, 'Yes', 'avg_time')
            col3.metric('Tempo Médio c/ Festival', df1_aux.values[0] )

        with col4:
            df1_aux = avg_std_time_delivery (df1, 'Yes', 'std_time')
            col4.metric('Desvio Médio c/ Festival', df1_aux.values[0])

        with col5:
            df1_aux = avg_std_time_delivery (df1, 'No', 'avg_time')
            col5.metric('Tempo Médio de entrega s/ Festival', df1_aux.values[0])

        with col6:
            df1_aux = avg_std_time_delivery (df1, 'No', 'std_time')
            col6.metric('Desvio padrão s/ Festival', df1_aux.values[0])

    with st.container():
        st.sidebar.markdown("""---""")
        st.title('Distribuição do Tempo')

        col1, col2 = st.columns(2)

        with col1:
            fig = avg_std_time_graph(df1)
            st.plotly_chart( fig )


        with col2:
            fig = avg_std_time_on_traffic (df1)
            st.plotly_chart(fig)

            