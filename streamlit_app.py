# importing packages
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")
from PIL import Image
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
import plotly.io as pio
import app_functions as app
pd.options.display.float_format = "{:,.2f}".format


# SideBar Options
df_territory = app.load_df_territory()
uf = st.sidebar.selectbox(label='UF', options=df_territory.uf.unique())
options = app.filter_municipalities_by_uf(uf=uf, df=df_territory)
municipio = st.sidebar.selectbox(label='Município', options=options)
cod_municipio = app.get_cod_municipio(df=df_territory, uf=uf, municipio=municipio)
municipio_name = app.load_mun_name(cod_municipio=cod_municipio)


st.markdown(f"<h1 style='text-align: right; color: black;'>PopApp</h1>", unsafe_allow_html=True)
st.markdown(f'## {municipio}')

df_urbrur_growth = app.load_urbrur_data()

fig_urbrur_growth, ano_min, ano_max = app.plot_urbrur_growth(df=df_urbrur_growth, cod_municipio=cod_municipio)



@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_pop_growth_rate(df, cod_municipio):
    t0 = df[(df['Código'] == cod_municipio) & (df['Ano'] == 2000) & (df['Situação'] == 'Total')]['População'].values
    t = df[(df['Código'] == cod_municipio) & (df['Ano'] == 2010) & (df['Situação'] == 'Total')]['População'].values
    pop_growth_rate = round((((t/t0)**(1/10)-1) * 100)[0], 2)
    
    return pop_growth_rate




col_a, col_b = st.beta_columns((1, 6))
urb_indicator = app.get_urbanization_index(df=df_urbrur_growth, cod_municipio=cod_municipio)
if 2000 not in df_urbrur_growth[df_urbrur_growth['Código'] == cod_municipio].Ano.unique():
    urb_index = app.plot_urbanization_index(urb_indicator=urb_indicator, height=184, font_size=50, color=px.colors.qualitative.Plotly[0])
    col_a.markdown(f"<p style='text-align: left; color: black; font-size:18px'><b>Taxa de Urbanização<b></p>", unsafe_allow_html=True)
    col_a.plotly_chart(urb_index, use_container_width=True)
else:
    col_a.markdown(f"<p style='text-align: left; color: black; font-size:18px; line-height: 2'><b>Taxa de Urbanização<b></p>", unsafe_allow_html=True)
    urb_index = app.plot_urbanization_index(urb_indicator=urb_indicator, height=53, font_size=30, color=px.colors.qualitative.Plotly[0])
    col_a.plotly_chart(urb_index, use_container_width=True)
    pop_growth_rate = get_pop_growth_rate(df=df_urbrur_growth, cod_municipio=cod_municipio)
    indicator_pop_rate = app.plot_urbanization_index(urb_indicator=pop_growth_rate, height=53, font_size=30, color=px.colors.qualitative.Plotly[0])
    col_a.markdown(f"<p style='text-align: left; color: black; font-size:18px; margin-top: 10px; margin-bottom: 10px'><b>Taxa de Crescimento<b></p>", unsafe_allow_html=True)
    col_a.plotly_chart(indicator_pop_rate, use_container_width=True)


if uf == 'PR':
    df_projection = app.load_projection_data()
    subplots = app.subplot_pop_growth(df_urbrur=df_urbrur_growth, df_projection=df_projection, cod_municipio=cod_municipio)
    col_b.plotly_chart(subplots, use_container_width=True)

else:
#    st.plotly_chart(fig_urbrur_growth, use_container_width=True)
#    col_a, col_b = st.beta_columns((1, 4))
#    col_a.markdown(f"<p style='text-align: left; color: black; font-size:18px'><b>Taxa de Urbanização<b></p>", unsafe_allow_html=True)
#    col_b.markdown('**Taxa de Urbanização**')
    col_b.plotly_chart(fig_urbrur_growth, use_container_width=True)


df_estrutura_etaria_f, df_estrutura_etaria_m = app.load_age_groups()

fig_age_groups, year = app.plot_pop_pyramid(df_estrutura_etaria_f=df_estrutura_etaria_f, df_estrutura_etaria_m=df_estrutura_etaria_m, cod_municipio=cod_municipio, year=2010)

c1, c2 = st.beta_columns(2)

c1.plotly_chart(fig_age_groups, use_container_width=True)


gdf1 = app.load_sector_geodataframe(uf=uf, cod_municipio=cod_municipio)

fig_map1 = app.plot_density_map(gdf=gdf1)

c2.plotly_chart(fig_map1, use_container_width=True)

def plot_arranjo(cod_municipio):
    df = pd.read_csv('data/pop/arranjos populacionais/tab01.csv', sep=';', decimal=',', thousands='.')
    cod_arranjo = str(df[df['Código do município'] == cod_municipio]['CodArranjo'].values[0])
    
    gdf = gpd.read_file(f'data/territorio/municipalities/arranjos_pop/{cod_arranjo}/arranjo_{cod_arranjo}_municipalities.zip/')

    lon = gdf.dissolve(by='CodArranjo').centroid.x[0]
    lat = gdf.dissolve(by='CodArranjo').centroid.y[0]

    minx, miny, maxx, maxy = gdf.total_bounds
    max_bound = max(abs(maxx-minx), abs(maxy-miny)) * 111
    zoom = 12.7 - np.log(max_bound)

    fig_map = px.choropleth_mapbox(
        data_frame=gdf
        , geojson=gdf.geometry
    #    , featureidkey=gdf.index
        , locations=gdf.index
    #    , hover_name='CD_GEOCODI'
        , hover_data=None
        , zoom=zoom
        ,center={"lat": lat, "lon": lon}
        , mapbox_style="carto-positron"
        , title=f'<b>Arranjo Populacional de {gdf.NomeArranj[0]}<b>'
        , template=None
        , width=None
        , height=400
        , opacity=0.3
        )

    fig_map.update_layout(margin=dict(l=0, r=0, b=40, t=40))
    fig_map.layout.title.font.size = 18
    fig_map.update_traces(marker_line_width=0.1)
    return fig_map
df = pd.read_csv('data/pop/arranjos populacionais/tab01.csv', sep=';', decimal=',', thousands='.')
if cod_municipio in df['Código do município'].unique():
    fig_arranjo = plot_arranjo(cod_municipio=cod_municipio)
    st.plotly_chart(fig_arranjo, use_container_width=True)




