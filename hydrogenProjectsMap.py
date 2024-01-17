import pandas as pd
import folium
from IPython.display import display
import openrouteservice as ors
import branca
from folium.plugins import GroupedLayerControl


def excelReader(name):
    dataframe = pd.read_excel(name, index_col=None, header=1)
    return dataframe

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
    # The following adds a fullscreen button
    folium.plugins.Fullscreen(
        position="topright",
        title="Expand",
        title_cancel="Exit",
        force_separate_button=True,
    ).add_to(m)

    fg1 = folium.FeatureGroup(name='I drift', show=False)
    fg2 = folium.FeatureGroup(name='Första spadtaget', show=False)
    fg3 = folium.FeatureGroup(name='Projektering')
    fg4 = folium.FeatureGroup(name='Förstudie', show=False)
    fg5 = folium.FeatureGroup(name='Idéstadie', show=False)
    fg6 = folium.FeatureGroup(name='Övrigt')
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
            if row.get("Status") == "Anläggning i drift":
                folium.Marker(
                    location=list(reversed(result['geometry']['coordinates'])),
                    icon=folium.Icon(icon='compass', color="green", prefix='fa'),
                    popup=folium.Popup(iframe)
                ).add_to(fg1)
            elif row.get("Status") == "Första spadtaget":
                folium.Marker(
                    location=list(reversed(result['geometry']['coordinates'])),
                    icon=folium.Icon(icon='compass', color="lightgreen", prefix='fa'),
                    popup=folium.Popup(iframe)
                ).add_to(fg2)
            elif row.get("Status") == "Projektering":
                folium.Marker(
                    location=list(reversed(result['geometry']['coordinates'])),
                    icon=folium.Icon(icon='compass', color="beige", prefix='fa'),
                    popup=folium.Popup(iframe)
                ).add_to(fg3)
            elif row.get("Status") == "Förstudie":
                folium.Marker(
                    location=list(reversed(result['geometry']['coordinates'])),
                    icon=folium.Icon(icon='compass', color="lightred", prefix='fa'),
                    popup=folium.Popup(iframe)
                ).add_to(fg4)
            elif row.get("Status") == "idestadie":
                folium.Marker(
                    location=list(reversed(result['geometry']['coordinates'])),
                    icon=folium.Icon(icon='compass', color="red", prefix='fa'),
                    popup=folium.Popup(iframe)
                ).add_to(fg5)
            else:
                folium.Marker(
                    location=list(reversed(result['geometry']['coordinates'])),
                    icon=folium.Icon(icon='compass', color="lightgray", prefix='fa'),
                    popup=folium.Popup(iframe)
                ).add_to(fg6)

    m.add_child(fg1)
    m.add_child(fg2)
    m.add_child(fg3)
    m.add_child(fg4)
    m.add_child(fg5)
    m.add_child(fg6)

    GroupedLayerControl(
        groups={'Status': [fg1, fg2, fg3, fg4, fg5, fg6]},
        exclusive_groups=False,
        collapsed=False,
    ).add_to(m)

    m.save("HydrogenProjects.html")

name = 'Vatgasprojekt.xlsx'
APIkey = "5b3ce3597851110001cf62489ed672afecf3475d8209f79cdb8f560e"
mapCreator(APIkey,excelReader(name))
