import pandas as pd
import folium
from IPython.display import display
import openrouteservice as ors
import branca

def excelReader(name):
    dataframe = pd.read_excel(name, index_col=None, header=1)
    return dataframe

def colorPicker(status):
    color = "lightgray"
    if status == "Anläggning i drift":
        color = "green"
    elif status == "Första spadtaget":
        color = "lightgreen"
    elif status == "Projektering":
        color = "beige"
    elif status == "Förstudie":
        color = "lightred"
    elif status == "idestadie":
        color = "red"
    return color

def description(row):
    html = "" ""
    i = 3
    for index in row[3:-1]:
        if isinstance(index, str):
            html += "<b>"+row.index[i]+": </b>"+index+"<br>"
        elif index>0:
            html += "<b>" + row.index[i] + ": </b>" + str(index) + "<br>"
        i += 1
    return html

def mapCreator(api, df):
    client = ors.Client(key=api)
    m = folium.Map(location=[62, 15], tiles='OpenStreetMap', zoom_start=8)
    for index, row in df.iterrows():
        geocode = client.pelias_search(
            text=row.get("Ort"),
            focus_point=list(reversed(m.location)),
            country="SE",
            size=1,
            validate=False,
        )
        for result in geocode['features']:
            iframe = branca.element.IFrame(html=description(row), width=500, height=300)
            folium.Marker(
                location=list(reversed(result['geometry']['coordinates'])),
                icon=folium.Icon(icon='compass', color=colorPicker(row.get("Status")), prefix='fa'),
                popup=folium.Popup(iframe)
            ).add_to(m)

    m.save("HydrogenProjects.html")

name = 'Vatgasprojekt.xlsx'
APIkey = "5b3ce3597851110001cf62489ed672afecf3475d8209f79cdb8f560e"
mapCreator(APIkey,excelReader(name))
