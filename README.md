# PopApp
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/augustogeog/popapp/main)

A Web App that presents a dashaboard with indicators, plots and cartographic representations related to population of Brazilian municipalities.

![alt text](https://github.com/augustogeog/popapp/raw/main/data/gif/gif.gif "App")


## Repo Structure

* **Notebooks**
    * census_microdata.ipynb (scripts to collect census microdata and save treated files related to commuting)
    * commuting_kepler.ipynb (generation of the kepler.gl object for rendering commuting maps)
    * geodata.ipynb (scripts to collect and treat shapefiles of Brazilian municipalities, besides development of functions used in the app_functions)
* **Python Files**
    * streamlit_app (aplication layout and functions calls to render indicators, maps and plots)
    * app_functions (functionalities designed to retrieve dataframes, geodatrafames and plot correspondent information into the streamlit_app)
    * geodata.py (functions used in the geodata.ipynb notebook to retrieve and treat geoespatial data)
* **Directories**
    * Data (data used in the webapp)
        * pop (population data)
            * arranjos populacionais (base of urban aglomerations that encompass several municipalities)
            * commuting (data related to origins and destinations of communters in brazilian urban aglomerations)
            * microdata amostra (censitary microdata)
            * setores (population data organized by censitary sector, areas used as reference to collect censitary data)
        * territorio (geospatial data, like shapefiles and csv files with the territorial structure of refference)
        * gif (gif used in the read-me file)


