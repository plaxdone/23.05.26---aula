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
print(cuslocordite_prod)
cuslocordite_pop = cuslocordite_prod.merge(dfs['populacao'], how='inner', on='customer_city')
print(cuslocordite_pop)
cuslocordite_rev= cuslocordite_pop.merge(dfs['review'], how='left', on='order_id')

# Selecionando as colunas de interesse
final = cuslocordite_rev[['customer_id', 'customer_unique_id', 'customer_zip_code_prefix',
       'customer_city', 'pop', 'customer_state',
       'geolocation_lat', 'geolocation_lng','order_id', 'order_status',
       'order_purchase_timestamp', 'order_approved_at',
       'order_delivered_carrier_date', 'order_delivered_customer_date',
       'order_estimated_delivery_date', 'order_item_id', 'product_id',
       'seller_id', 'shipping_limit_date', 'price', 'freight_value',
       'product_category_name', 'product_photos_qty',
       'review_id', 'review_score', 'review_comment_title',
       'review_comment_message', 'review_creation_date',
       'review_answer_timestamp']]

# Convertendo para datetime
datas = ['order_purchase_timestamp'
        ,'order_purchase_timestamp'
        ,'order_delivered_carrier_date'
        ,'order_delivered_customer_date'
        ,'order_estimated_delivery_date'
        ,'shipping_limit_date'
        ,'review_creation_date'
        ,'review_answer_timestamp' 
        ]

for data in datas:
    final[data] = pd.to_datetime(final[data])

# Criando coluna de tempo de entrega e Hora da compra
tempo_entrega = final['order_delivered_customer_date'].dt.date
hora_compra = final['order_purchase_timestamp'].dt.date

tmp = tempo_entrega - hora_compra
tmp = tmp.fillna(0)

ll = [x.days if type(x) is timedelta else int(x)  for x in tmp.to_list()]
final['delivery_time'] = ll

# Seleção do período de interesse
final = final[(final['order_purchase_timestamp'].dt.year > 2016) 
              & 
              (final['order_purchase_timestamp'] < pd.to_datetime('20180901'))
              &
              (final['customer_state'] == 'PR')
              &
              (final['price'] <= 200)
             ]
final = final.reset_index(drop=True)
# final.info()
final.to_csv("dataPR3.csv")