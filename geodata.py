import geopandas as gpd
import pandas as pd
import plotly.express as px
import json
import numpy as np
import plotly.io as pio
import os
from zipfile import ZipFile
from urllib import request
pd.options.display.float_format = "{:,.2f}".format


def donwload_sectors_shp_2010(ufs):

    try:
        for uf in ufs:
            if uf == 'GO':
                remote_url = f'https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_de_setores_censitarios__divisoes_intramunicipais/censo_2010/setores_censitarios_shp/go/go_setores%20_censitarios.zip'
                dirs = f'data/territorio/setores2010/{uf}/'
                os.makedirs(dirs, exist_ok=True)
                file = dirs+ f'{uf.lower()}_setores_censitarios.zip'
                request.urlretrieve(remote_url, file)
                with ZipFile(file, "r") as z:
                    z.extractall(dirs)
                print(uf + ' done!')

            else:
                remote_url = f'https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_de_setores_censitarios__divisoes_intramunicipais/censo_2010/setores_censitarios_shp/{uf.lower()}/{uf.lower()}_setores_censitarios.zip'
                dirs = f'data/territorio/setores2010/{uf}/'
                os.makedirs(dirs, exist_ok=True)
                file = dirs+ f'{uf.lower()}_setores_censitarios.zip'
                request.urlretrieve(remote_url, dirs+ f'{uf.lower()}_setores_censitarios.zip')
                with ZipFile(file, "r") as z:
                    z.extractall(dirs)
                print(uf + ' done!')
    except:
        print('An exception occurred. Probably related to the internet conection. It also can be the case that IBGE changed the data urls.')


def download_sector_statistics_2010(ufs):
    try:
        for uf in ufs:
            if uf == 'SP':
                
                for territory in ['SP_Exceto_a_Capital_20190207.zip', 'SP_Capital_20190823.zip']:
                    remote_url = f'https://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/{territory}'            
                    dirs = f'data/pop/setores/{uf.upper()}/'
                    os.makedirs(dirs, exist_ok=True)
                    file = dirs+ territory
                    request.urlretrieve(remote_url, file)
                    with ZipFile(file, "r") as z:
                        z.extractall(dirs)
                    print(uf + ' done!')
            
            elif uf == 'PE':
                remote_url = f'https://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/PE_20200219.zip'            
                dirs = f'data/pop/setores/{uf.upper()}/'
                os.makedirs(dirs, exist_ok=True)
                file = dirs+ f'PE_20200219.zip'
                request.urlretrieve(remote_url, file)
                with ZipFile(file, "r") as z:
                    z.extractall(dirs)
                print(uf + ' done!')           
            
            
            else:
                remote_url = f'https://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/{uf.upper()}_20171016.zip'            
                dirs = f'data/pop/setores/{uf.upper()}/'
                os.makedirs(dirs, exist_ok=True)
                file = dirs+ f'{uf.upper()}_20171016.zip'
                request.urlretrieve(remote_url, file)
                with ZipFile(file, "r") as z:
                    z.extractall(dirs)
                print(uf + ' done!')
    except:
        print('An exception occurred. Probably related to the internet conection. It also can be the case that IBGE changed the data urls.')


def treat_sectors_shp(uf):
    
    dict_ufs = {
        'RO':'11',
        'AC':'12',
        'AM':'13',
        'RR':'14',
        'PA':'15',
        'AP':'16',
        'TO':'17',
        'MA':'21',
        'PI':'22',
        'CE':'23',
        'RN':'24',
        'PB':'25',
        'PE':'26',
        'AL':'27',
        'SE':'28',
        'BA':'29',
        'MG':'31',
        'ES':'32',
        'RJ':'33',
        'SP':'35',
        'PR':'41',
        'SC':'42',
        'RS':'43',
        'MS':'50',
        'MT':'51',
        'GO':'52',
        'DF':'53'
    }
    
    gdf = gpd.read_file(f'data/territorio/setores2010/{uf}/{dict_ufs[uf]}SEE250GC_SIR.shp')

    gdf = gdf.to_crs("EPSG:5880")

    gdf.rename(columns={'CD_GEOCODI':'Cod'}, inplace=True)

    gdf.drop(labels=['ID', 'CD_GEOCODS', 'NM_SUBDIST', 'CD_GEOCODD', 'NM_DISTRIT', 'NM_MICRO', 'NM_MESO'], axis=1, inplace=True)

    if uf.upper() == 'PE':
        df_pb_pop = pd.read_csv(f'data/pop/setores/PE/PE_20171016/PE/Base informaçoes setores2010 universo {uf.upper()}/CSV/Basico_{uf.upper()}.csv', sep=';', usecols=['Cod_setor', 'V002'],encoding='ANSI')
    elif uf.upper() == 'ES':
        df_pb_pop = pd.read_csv(f'data/pop/setores/ES/Base informaçoes setores2010 universo {uf.upper()}/CSV/Basico_{uf.upper()}.csv', sep=';', usecols=['Cod_setor', 'V002'],encoding='ANSI')
    elif uf.upper() == 'TO':
        df_pb_pop = pd.read_csv(f'data/pop/setores/TO/Base informacoes setores2010 universo TO/CSV/Basico_{uf.upper()}.csv', sep=';', usecols=['Cod_setor', 'V002'],encoding='ANSI')
    elif uf.upper() == 'RS':
        df_pb_pop = pd.read_csv(f'data/pop/setores/RS/RS_20150527/RS/Base informaçoes setores2010 universo {uf.upper()}/CSV/Basico_{uf.upper()}.csv', sep=';', usecols=['Cod_setor', 'V002'],encoding='ANSI')
    elif uf.upper() == 'SP':        
        df_pb_pop = pd.read_csv(f'data/pop/setores/SP/Base informaçoes setores2010 universo SP_Capital/CSV/Basico_SP1.csv', sep=';', usecols=['Cod_setor', 'V002'],encoding='ANSI')
        df_pb_pop2 = pd.read_csv(f'data/pop/setores/SP/SP Exceto a Capital/Base informaçoes setores2010 universo SP_Exceto_Capital/CSV/Basico_SP2.csv', sep=';', usecols=['Cod_setor', 'V002'],encoding='utf-8')
        df_pb_pop = pd.concat(objs=[df_pb_pop, df_pb_pop2])
        df_pb_pop.reset_index(drop=True, inplace=True)
    else:
        df_pb_pop = pd.read_csv(f'data/pop/setores/{uf.upper()}/{uf.upper()}/Base informaçoes setores2010 universo {uf.upper()}/CSV/Basico_{uf.upper()}.csv', sep=';', usecols=['Cod_setor', 'V002'],encoding='ANSI')

    df_pb_pop.columns = ['Cod', 'Pop']

    df_pb_pop['Cod'] = df_pb_pop.Cod.astype(np.int64)

    df_pb_pop['Pop'].fillna(value=0, inplace=True)

    df_pb_pop['Pop'] = df_pb_pop['Pop'].astype(np.int64)

    gdf['Cod'] = gdf.Cod.astype(np.int64)

    gdf = gdf.merge(df_pb_pop, on='Cod', how='left')

    gdf['Pop'].fillna(value=0, inplace=True)

    gdf['Pop'] = gdf['Pop'].astype(np.int64)

    gdf['Area'] = gdf.area / 10000

    gdf['Pop/ha'] = gdf['Pop'] / gdf['Area']

    gdf1 = gpd.read_file(f'data/territorio/setores2010/{uf}/{dict_ufs[uf]}SEE250GC_SIR.shp')

    gdf1.drop(labels=['ID', 'CD_GEOCODS', 'NM_SUBDIST', 'CD_GEOCODD', 'NM_DISTRIT', 'NM_MICRO', 'NM_MESO'], axis=1, inplace=True)

    gdf1.rename(columns={'CD_GEOCODI':'Cod'}, inplace=True)

    gdf1['Cod'] = gdf1['Cod'].astype(np.int64)

    gdf1 = gdf1.merge(right=gdf[['Cod', 'Pop', 'Area', 'Pop/ha']], on='Cod', how='left')            
    
    return gdf1

def save_sectors_geodataframe(gdf, uf):
    for cod_mun in gdf['CD_GEOCODM'].unique():
        try:
            os.makedirs(f'data/territorio/setores2010/{uf}/{cod_mun}/', exist_ok=True)
            gdf.loc[gdf['CD_GEOCODM'] == cod_mun].to_file(f'data/territorio/setores2010/{uf}/{cod_mun}/{cod_mun}.shp')
        except:
            print(f'Exception while saving {cod_mun}.shp')
    print(f'files saved.')