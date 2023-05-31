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

df = pd.read_csv("dataPR3.csv", na_values=[" "])

#Seleção de informações agrupadas pelo consumidor
cus_valor = df.groupby('customer_city', as_index=False)['price'].sum() #price_x
med_valor = df.groupby('customer_city', as_index=False)['price'].mean()
pop = df.groupby('customer_city', as_index=False)['pop'].mean()
med_valor = med_valor.rename(columns={'price':'med_price'})
cus_qtd = df.groupby('customer_city', as_index=False)['price'].count() #price_y
cus_frete = df.groupby('customer_city', as_index=False)['freight_value'].sum()
med_frete = df.groupby('customer_city', as_index=False)['freight_value'].mean()
med_frete = med_frete.rename(columns={'freight_value':'med_freight_value'})



#União das informações em um Dataframe
customer = cus_valor.merge(med_valor, on='customer_city')
customer = customer.merge(cus_qtd, on='customer_city')
customer = customer.merge(pop, on='customer_city')
customer = customer.merge(cus_frete, on='customer_city')
customer = customer.merge(med_frete, on='customer_city')
customer = customer.rename(columns={'price_x':'price', 'price_y':'count_items'})


print(customer.sort_values(by='price', ascending=False).head(10))