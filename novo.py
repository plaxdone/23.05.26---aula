# We first import the libraries. 
import pandas as pd
import folium, webbrowser
from folium.plugins import StripePattern
import geopandas as gpd
import numpy as np
# Next we import the data. 
df = pd.read_csv("dataPR.csv")

# We grab the state and wills column
df = df[["customer_city", "price"]]
# print(len(df))
# print(df.head())

# We import the geoJSON file. 
state_geo = "new_munic.json"

# We read the file and print it.
geoJSON_df = gpd.read_file(state_geo)
# print(geoJSON_df.head())

# we rename the column from id to state in the geoJSON_df so we can merge the two data frames.
geoJSON_df = geoJSON_df.rename(columns = {"NOME":"customer_city"})
# Next we merge our sample data (df) and the geoJSON data frame on the key id.
final_df = geoJSON_df.merge(df, on = "customer_city")
# print(len(final_df))

m = folium.Map(location=[-24,-51], zoom_start=7)

# Set up Choropleth map
folium.Choropleth(
geo_data=final_df,
data=final_df,
columns=["customer_city", "price"],
key_on="feature.properties.customer_city",
fill_color='YlGnBu',
fill_opacity=1,
line_opacity=0.2,
legend_name="Valor gasto (%)",
smooth_factor=0,
Highlight= True,
line_color = "#0000",
name = "choropleth",
show=False,
overlay=True,
nan_fill_color = "White"
).add_to(m)

# We import the required library:
from branca.element import Template, MacroElement

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legend (draggable!)</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:white;opacity:0.7;'></span>States that have Null values.</li>
    

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

m.get_root().add_child(macro)

# We create another map called sample_map2.
sample_map2 = folium.Map(location=[-24,-51], zoom_start=7)

# Set up Choropleth map
folium.Choropleth(
geo_data=final_df,
data=final_df,
columns=["customer_city", "price"],
key_on="feature.properties.customer_city",
fill_color='YlGnBu',
fill_opacity=1,
line_opacity=0.2,
legend_name="Valor gasto (%)",
smooth_factor=0,
Highlight= True,
line_color = "#0000",
name = "choropleth",
show=True,
overlay=True,
nan_fill_color = "White"
).add_to(sample_map2)



# Here we add cross-hatching (crossing lines) to display the Null values.
nans = final_df[final_df["price"].isnull()]['customer_city'].values
gdf_nans = final_df[final_df['customer_city'].isin(nans)]
sp = StripePattern(angle=45, color='grey', space_color='white')
sp.add_to(sample_map2)
folium.features.GeoJson(name="Click for Wills NaN values",data=gdf_nans, style_function=lambda x :{'fillPattern': sp},show=True).add_to(sample_map2)

# We add a layer controller. 
folium.LayerControl(collapsed=False).add_to(sample_map2)
sample_map2

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
sample_map2.add_child(NIL)
sample_map2.keep_in_front(NIL)





sample_map2.save("map.html")
webbrowser.open("map.html")