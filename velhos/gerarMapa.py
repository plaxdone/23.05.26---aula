import pandas as pd
import geopandas as gpd
import folium, webbrowser
import matplotlib.pyplot as plt
df = pd.read_csv("./data/dataPR2.csv", na_values=[" "])
df = df[["customer_city", "price"]]


mun_geo = "./geoJson/new_munic.json"
state_geo = "Brasil.json"
pr_geo = "PR.json"

geoJSON_df = gpd.read_file(mun_geo)

geoJSON_df = geoJSON_df.rename(columns = {"NOME":"customer_city"})
final_df = geoJSON_df.merge(df, on = "customer_city")
#print(final_df)

fig, ax = plt.subplots(1, figsize=(8, 8))
#plt.xticks(rotation=90)

final_df.plot(column="price", cmap="PiYG", linewidth=0.4, ax=ax, edgecolor=".4")
min = df['price'].min()
max = df['price'].max()
#print(min)
bar_info = plt.cm.ScalarMappable(cmap="PiYG", norm=plt.Normalize(vmin=min, vmax=max))
bar_info._A = []
cbar = fig.colorbar(bar_info)

plt.show()


# mymap = folium.Map(location=[-24,-51], zoom_start=7)

# folium.Choropleth(
#     name="choropleth",
#     data=final_df,
    
#     # geo_data=state_geo,  
#     # columns=["customer_state", "price"],
#     # key_on="feature.properties.UF",

#     geo_data=final_df,
#     columns=["customer_city", "price"],
#     key_on="feature.properties.customer_city",

#     fill_color="Greys",
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name="Valor gasto em R$",
#     smooth_factor=0,
#     Highlight= True,
#     line_color = "#ffffff",
#     #show=False,
#     overlay=True,
#     nan_fill_color = "white"
# ).add_to(mymap)

# # Add hover functionality.
# style_function = lambda x: {'fillColor': '#ffffff', 
#                             'color':'#000000', 
#                             'fillOpacity': 0.1, 
#                             'weight': 0.1}
# highlight_function = lambda x: {'fillColor': '#000000', 
#                                 'color':'#000000', 
#                                 'fillOpacity': 0.50, 
#                                 'weight': 0.1}
# NIL = folium.features.GeoJson(
#     data = final_df,
#     style_function=style_function, 
#     control=False,
#     highlight_function=highlight_function, 
#     tooltip=folium.features.GeoJsonTooltip(
#         fields=['customer_city','price'],
#         aliases=['customer_city','price'],
#         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
#     )
# )
# mymap.add_child(NIL)
# mymap.keep_in_front(NIL)



# folium.LayerControl().add_to(mymap)


# mymap.save("map.html")
# webbrowser.open("map.html")