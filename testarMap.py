import folium
import webbrowser

# Crie o mapa com a localidade de seu interesse.
m = folium.Map(location=[-15.793889, -47.882778], zoom_start=11)
m.save("map.html")
webbrowser.open("map.html")