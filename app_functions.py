import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
import plotly.io as pio



@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def subplot_pop_growth(df_urbrur=None, df_projection=None, cod_municipio=4125506):
    """
    Under development
    """

    df_urbrur = df_urbrur.loc[df_urbrur["Código"] == cod_municipio]
    df_pop_total = df_urbrur[df_urbrur['Situação'] == 'Total']
    df_pop_urbana = df_urbrur[df_urbrur['Situação'] == 'Urbana']
    df_pop_rural = df_urbrur[df_urbrur['Situação'] == 'Rural']

    df_projection = df_projection.loc[df_projection["Código"] == cod_municipio]
    df_projection = df_projection.sort_values(by='Ano')

    subplots = make_subplots(
        rows=1
        , cols=2
        , shared_xaxes=True
        , shared_yaxes=True
        , horizontal_spacing=0.06        
        , subplot_titles=("1970 e 2010", "2010 a 2040"))
    subplots.append_trace(go.Scatter(x=df_pop_total['Ano'], y=df_pop_total['População'], name='Total'), row=1, col=1)
    subplots.append_trace(go.Scatter(x=df_pop_urbana['Ano'], y=df_pop_urbana['População'], name='Urbana'), row=1, col=1)
    subplots.append_trace(go.Scatter(x=df_pop_rural['Ano'], y=df_pop_rural['População'], name='Rural'), row=1, col=1)
    subplots.append_trace(go.Scatter(x=df_projection['Ano'], y=df_projection['População'], name='Projetada'), row=1, col=2)
    subplots.update_layout(width=1200, height=250, title_text='<b>Crescimento Demográfico<b>')
    subplots.update_layout(font=dict(size=10))
    subplots.update_layout(margin=dict(l=0, r=0, b=0, t=50))
    subplots.layout.title.font.size = 18
    

#    ano_min = df['Ano'].min()
#    ano_max = df['Ano'].max()

    return subplots


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_mun_name(cod_municipio=4125506):
    municipios = pd.read_csv('data/territorio/municipios_brasileiros.csv', sep=';')
    
    name_municipio = municipios[municipios['cod'] == cod_municipio]['municipio'].values[0]

    return name_municipio



@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_urbrur_data():
    """
    Loads data from the file pop_urbano_rural_total_70_10.CSV into a Pandas DataFrame. Treats the data so it can be used as an argument to devise a line plot with the plot_urbrur_growth function.
    pop_urbano_rural_total_70_10.CSV must be in the folder data/pop/.
    """

    df = pd.read_csv(
        "data/pop/pop_urbano_rural_total_70_10.CSV",
        sep=";",
        dtype={
            "codmun": np.int32,
            "nomemun": "object",
            "ano": np.int32,
            "Total": np.int32,
            "Urbana": np.int32,
            "Rural": np.int32,
        },
    )
    df = df.melt(id_vars=["codmun", "nomemun", "ano"])
    df.columns = ["Código", "Município", "Ano", "Situação", "População"]

    return df


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def plot_urbrur_growth(df=None, cod_municipio=4125506):
    """
    Generates a line plot of the rural, urban an total population of the selected municipality.
    The df argument must be the Pandas DataFrame generated by the function load_urbrur_data.
    cod_municipio must be an integer representing the IBGE code for the municipality of interest.
    """

    df = df.loc[df["Código"] == cod_municipio]
    fig = px.line(data_frame=df, x="Ano", y="População", color="Situação", width=1300, height=270, title='<b>Variação Demográfica<b>')
    fig.update_layout(font=dict(size=18))
    ano_min = df['Ano'].min()
    ano_max = df['Ano'].max()
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=40))
    fig.layout.title.font.size = 18
    fig.update_layout(xaxis_tickfont_size=12, yaxis_tickfont_size=12, xaxis_title_font_size=14, yaxis_title_font_size=14, legend_font_size=12, legend_title_font_size=14)


    return fig, ano_min, ano_max


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_projection_data():
    """
    Loads projection data into a Pandas DataFrame to be used as an argument in the plot_projection function.

    """

    dict_types = {
        "codmun": np.int32,
        "nomemun": "object",
        "2010": np.int32,
        "2020": np.int32,
        "2030": np.int32,
        "2040": np.int32,
    }
    df = pd.read_csv(
        "data/pop/pop_projetada_ipardes_consolidada.csv", sep=";", dtype=dict_types
    )
    df = df.melt(id_vars=["codmun", "nomemun"])
    df.columns = ["Código", "Município", "Ano", "População"]

    return df


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def plot_projection(df=None, cod_municipio=4125506):
    """
    Generates a line plot of the population projecte to the next decades by the IPARDES.
    The df argument must be the Pandas DataFrame generated by the load_projection_data function.
    cod_municipio must be an integer representing the IBGE code for the municipality of interest.

    """
    df = df.loc[df["Código"] == cod_municipio]
    df = df.sort_values(by="Ano")
    proj_max = df['Ano'].max()


    fig = px.line(data_frame=df, x="Ano", y="População", width=1300, height=400)

    return fig, proj_max


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_urbanization_index(df, cod_municipio):
    """
    Returns the urbanization index for the municipality whose IBGE code is provided in cod_municipio.
    The df argument must be the Pandas DataFrame generated by the function load_urbrur_data.
    """

    df = df.loc[(df["Código"] == cod_municipio) & (df["Ano"] == df["Ano"].max())]
    urban_pop = df.loc[df["Situação"] == "Urbana"]["População"].values
    total_pop = df.loc[df["Situação"] == "Total"]["População"].values
    urbanization_index = urban_pop / total_pop * 100

    return round(urbanization_index[0], 2)


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_age_groups():

    dtypes = {
        "codmun": np.int32,
        "sexo": "category",
        "0 a 4 anos": np.int32,
        "5 a 9 anos": np.int32,
        "10 a 14 anos": np.int32,
        "15 a 19 anos": np.int32,
        "20 a 24 anos": np.int32,
        "25 a 29 anos": np.int32,
        "30 a 34 anos": np.int32,
        "35 a 39 anos": np.int32,
        "40 a 44 anos": np.int32,
        "45 a 49 anos": np.int32,
        "50 a 54 anos": np.int32,
        "55 a 59 anos": np.int32,
        "60 a 64 anos": np.int32,
        "65 a 69 anos": np.int32,
        "70 a 74 anos": np.int32,
        "75 a 79 anos": np.int32,
        "80 anos ou mais": np.int32,
    }

    df_estrutura_etaria = pd.read_csv("data/pop/estruturaetaria.csv", sep=";")

    df_estrutura_etaria = df_estrutura_etaria.melt(id_vars=["codmun", "sexo"])

    df_estrutura_etaria.columns = ["Código", "Sexo", "Faixa", "População"]
    
    df_estrutura_etaria_f = df_estrutura_etaria[df_estrutura_etaria['Sexo'] == 'Feminino']
    df_estrutura_etaria_m = df_estrutura_etaria[df_estrutura_etaria['Sexo'] == 'Masculino']

    return df_estrutura_etaria_f, df_estrutura_etaria_m


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def plot_pop_pyramid(df_estrutura_etaria_f, df_estrutura_etaria_m, cod_municipio, year):
    df_estrutura_etaria_f = df_estrutura_etaria_f[df_estrutura_etaria_f['Código'] == cod_municipio]
    df_estrutura_etaria_m = df_estrutura_etaria_m[df_estrutura_etaria_m['Código'] == cod_municipio]

    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, shared_xaxes=True, horizontal_spacing=0.0)

    sub0 = px.bar(data_frame=df_estrutura_etaria_f, y='Faixa', x='População', color='Sexo', orientation='h', color_discrete_map={'Feminino':'rgb(228, 26,28)'}, barmode='overlay')

    sub0.update_layout(xaxis_autorange='reversed')

    sub1 = px.bar(data_frame=df_estrutura_etaria_m, y='Faixa', x='População', orientation='h', color='Sexo', barmode='overlay')

    fig.add_traces(sub0['data'][0], rows=1, cols=1);
    fig.add_traces(sub1['data'][0], rows=1, cols=2);
    fig.data[0].showlegend= False
    fig.data[1].showlegend= False
    fig.layout.barmode = 'overlay'
    fig.layout.xaxis.autorange = 'reversed'
    fig.layout.xaxis.title.text = 'Feminino'
    fig.layout.xaxis2.title.text = 'Masculino'

    fig.layout.title.text = f'<b>         Pirâmide Etária<b>'
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=40)
    #, width=1075, height=400
    )
    fig.layout.title.font.size = 18
    fig.update_layout(height=400)

    return fig, year



@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_geo_dataframe(cod_municipio=4125506):
    
    if str(cod_municipio)[:2] == '41':
        file = 'data/territorio/setores_2010_pb.ftd'
    elif str(cod_municipio)[:2] == '25':
        file = 'data/territorio/setores_2010_pr.ftd'
    else:
        file = None
    
    if file != None:
        return gpd.read_feather(file)

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_df_territory():
    df_territory = pd.read_csv('data/territorio/municipios_brasileiros.csv', sep=';')
    return df_territory

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def filter_municipalities_by_uf(uf, df):
    options = df.municipio.loc[df.uf == uf].values
    return options

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_cod_municipio(df, uf, municipio):
    cod_municipio = df.loc[(df.uf == uf) & (df.municipio == municipio)]['cod'].values[0]
    return cod_municipio

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_plotly_map(file):
    return pio.read_json(file)

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_sector_geodataframe(uf,cod_municipio):
    cod_municipio = str(cod_municipio)
    gdf = gpd.read_file(f'data/territorio/setores2010/{uf}/{cod_municipio}/{cod_municipio}.shp')
    return gdf


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def plot_density_map(gdf):

#    gdf.drop(labels=['CD_GEOCODM', 'NM_MUNICIP', 'CD_GEOCODB'], axis=1, inplace=True)
    gdf['Pop/ha'] = gdf['Pop/ha'].fillna(0).astype(np.int64)
    gdf['Hab/ha'] = pd.cut(gdf['Pop/ha'], bins=[0, 10,25,50,75,100,9999999], labels=['Até 10', '10 a 25', '25 a 50', '50 a 75', '75 a 100', 'acima de 100'])
    gdf['Hab/ha'].fillna('Até 10', inplace=True)

    
    lon = gdf.dissolve(by='NM_MUNICIP').centroid.x[0]
    lat = gdf.dissolve(by='NM_MUNICIP').centroid.y[0]

    minx, miny, maxx, maxy = gdf.total_bounds
    max_bound = max(abs(maxx-minx), abs(maxy-miny)) * 111
    zoom = 13 - np.log(max_bound)

    fig_map = px.choropleth_mapbox(
        data_frame=gdf
        , geojson=gdf.geometry
    #    , featureidkey=gdf.index
        , locations=gdf.index
        , color='Hab/ha'
    #    , hover_name='CD_GEOCODI'
        , hover_data=None
        , zoom=zoom
        ,center={"lat": lat, "lon": lon}
        , mapbox_style="carto-positron"
        , title='<b>Densidade Demográfica<b>'
        , template=None
        , width=None
        , height=400
        , opacity=0.3
        , category_orders={'Hab/ha':['Até 10', '10 a 25', '25 a 50', '50 a 75', '75 a 100', 'acima de 100']}
        , color_discrete_sequence=px.colors.sequential.RdBu_r[5:]
        )
    
    fig_map.update_layout(margin=dict(l=0, r=0, b=40, t=40))
    fig_map.layout.title.font.size = 18

    return fig_map