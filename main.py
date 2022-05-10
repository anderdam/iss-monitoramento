import requests
import numpy as np
# import matplotlib.pyplot as plt
from datetime import datetime
from mpl_toolkits.basemap import Basemap
from drawnow import *

# API: http://www.n2yo.com/api
apiKey: str = 'LTDDZF-8R9TDP-KCSKWE-4VJC'


# Requisição de dados

def iss_station():
    norad_id = "25544"
    observer_lat = "41.702"
    observer_lon = "-76.014"
    observer_alt = "0"
    seconds = 2

    url = f'https://api.n2yo.com/rest/v1/satellite/positions/{norad_id}/{observer_lat}/{observer_lon}/{observer_alt}/' \
          f'{seconds}/&apiKey={apiKey}'
    response = requests.get(url)
    data = response.json()
    return data


# STREAMING DE DADOS DO ISS

def live_iss():
    iss = iss_station()
    longitude_iss = iss['positions'][0]['satlongitude']
    latitude_iss = iss['positions'][0]['satlatitude']

    # CONFIGURANDO A INSTANCIA BASEMAP
    worldmap = Basemap(projection='cyl', resolution='c', llcrnrlat='-90', urcrnrlat='90', llcrnrlon='-180',
                       urcrnrlon='180')

    worldmap.bluemarble()
    worldmap.drawcountries(linewidth=0.8, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
    worldmap.drawstates(linewidth=0.8, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
    worldmap.drawparallels(np.arange(-90, 90, 30), labels=[1, 1, 0, 1], fontsize=8)
    worldmap.drawmeridians(np.arange(-180, 180, 30), labels=[1, 1, 0, 1], fontsize=8, rotation=45)

    date = datetime.utcnow()
    worldmap.nightshade(date)

    # Plotando a ISS no mapa
    x, y = worldmap(longitude_iss, latitude_iss)
    plt.plot(x, y, '*', color='white', markersize=7)
    plt.text(x, y, 'ISS', color='white', fontsize=9)
    plt.title('Dia/Noite - %s (UTC)' % date.strftime('%d/%b/%Y %H:$M:%S'))
    plt.xlabel('Longitude', labelpad=40, fontsize=9)
    plt.ylabel('Latitude', labelpad=40, fontsize=9)


# CONSUMINDO A APLICAÇÃO
while True:
    drawnow(live_iss)
    plt.pause(1)
