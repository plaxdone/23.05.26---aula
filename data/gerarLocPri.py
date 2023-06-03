import pandas as pd
pd.options.display.float_format = '{:.2f}'.format
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
plt.style.use('fivethirtyeight')
import warnings
warnings.filterwarnings('ignore')
import folium
from folium import plugins
from sklearn.cluster import DBSCAN
from datetime import timedelta



files = {'customers'    : 'C:\\Users\\Jorge\\IFPR\\20 - Aprendizado de maquina\\23.05.26 - aula\\archive\\olist_customers_dataset.csv',
         'geolocation'  : 'C:\\Users\\Jorge\\IFPR\\20 - Aprendizado de maquina\\23.05.26 - aula\\archive\\olist_geolocation_dataset.csv',
         'items'        : 'C:\\Users\\Jorge\\IFPR\\20 - Aprendizado de maquina\\23.05.26 - aula\\archive\\olist_order_items_dataset.csv',
         'payment'      : 'C:\\Users\\Jorge\\IFPR\\20 - Aprendizado de maquina\\23.05.26 - aula\\archive\\olist_order_payments_dataset.csv',
         'orders'       : 'C:\\Users\\Jorge\\IFPR\\20 - Aprendizado de maquina\\23.05.26 - aula\\archive\\olist_orders_dataset.csv',
         'products'     : 'C:\\Users\\Jorge\\IFPR\\20 - Aprendizado de maquina\\23.05.26 - aula\\archive\\olist_products_dataset.csv',
         'sellers'      : 'C:\\Users\\Jorge\\IFPR\\20 - Aprendizado de maquina\\23.05.26 - aula\\archive\\olist_sellers_dataset.csv',
         'review'       : 'C:\\Users\\Jorge\\IFPR\\20 - Aprendizado de maquina\\23.05.26 - aula\\archive\\olist_order_reviews_dataset.csv',
         'populacao'    : 'C:\\Users\\Jorge\\IFPR\\20 - Aprendizado de maquina\\23.05.26 - aula\\archive\\populacao.csv',
         }

dfs = {}
for key, value in files.items():
    dfs[key] = pd.read_csv(value)


# Cruzamento gradativo
customers_location = dfs['customers'].merge(dfs['geolocation'], how='inner', left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix').drop_duplicates('customer_id', keep='first')
cusloc_order = customers_location.merge(dfs['orders'], how='inner', on='customer_id')
cuslocord_item = cusloc_order.merge(dfs['items'], how='inner', on='order_id')
cuslocordite_prod = cuslocord_item.merge(dfs['products'], how='inner', on='product_id')
cuslocordite_rev= cuslocordite_prod.merge(dfs['review'], how='left', on='order_id')

# Selecionando as colunas de interesse
final = cuslocord_item[['customer_id', 'customer_zip_code_prefix',
       'customer_city', 'customer_state',
       'geolocation_lat', 'geolocation_lng', 'price',]]



final = final.reset_index(drop=True)
# final.info()
final.to_csv("./data/locPri.csv")