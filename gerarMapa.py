import pandas as pd
import geopandas as gpd
import folium, webbrowser
df = pd.read_csv("dataPR.csv", na_values=[" "])
df = df[["customer_city", "price"]]

mun_geo = "new_munic.json"
state_geo = "Brasil.json"
pr_geo = "PR.json"

geoJSON_df = gpd.read_file(mun_geo)

geoJSON_df = geoJSON_df.rename(columns = {"NOME":"customer_city"})
final_df = geoJSON_df.merge(df, on = "customer_city")


m = folium.Map(location=[-24,-51], zoom_start=7)

folium.Choropleth(
    name="choropleth",
    data=final_df,
    
    # geo_data=state_geo,  
    # columns=["customer_state", "price"],
    # key_on="feature.properties.UF",

    geo_data=final_df,
    columns=["customer_city", "price"],
    key_on="feature.properties.customer_city",

    fill_color="Greys",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Valor gasto (%)",
    smooth_factor=0,
    Highlight= True,
    line_color = "#ffffff",
    #show=False,
    overlay=True,
    nan_fill_color = "white"
).add_to(m)

# Add hover functionality.
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
NIL = folium.features.GeoJson(
    data = final_df,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['customer_city','price'],
        aliases=['customer_city','price'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
m.add_child(NIL)
m.keep_in_front(NIL)



folium.LayerControl().add_to(m)


m.save("map.html")
webbrowser.open("map.html")