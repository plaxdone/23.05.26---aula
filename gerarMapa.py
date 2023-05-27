import pandas as pd
import folium, webbrowser
df = pd.read_csv("data.csv", na_values=[" "])

mun_geo = "municipio.json"
state_geo = "Brasil.json"


m = folium.Map(location=[-15,-51], zoom_start=4)

folium.Choropleth(
    name="choropleth",
    data=df,
    
    geo_data=state_geo,  
    columns=["customer_state", "price"],
    key_on="feature.properties.UF",

    #geo_data=mun_geo,
    #columns=["customer_city", "price"],
    #key_on="feature.properties.NOME",

    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Valor gasto (%)",
).add_to(m)

folium.LayerControl().add_to(m)


m.save("map.html")
webbrowser.open("map.html")