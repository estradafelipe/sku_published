#librerias
import requests
import pandas as pd
from datetime import datetime

#obtengo la lista de skus
skus_df = pd.read_csv('lista_sku.txt', header = None, names=["sku"])
#obtengo sku report
skuReport_df = pd.read_csv('skuReport.csv', encoding='latin-1')

#url busqueda de sku
url = "https://catalyst-uat.sodimac.com.ar/sodimac-ar/search?Ntt="
#url = "https://www.sodimac.com.uy/sodimac-uy/search?Ntt="
#url de busqueda sin resultados
noResult ='https://catalyst-uat.sodimac.com.ar/sodimac-ar/no-search-result?Ntt='
#noResult ='https://www.sodimac.com.ar/sodimac-uy/no-search-result?Ntt='

#header para la consulta al sitio
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.3"}

#lista donde se van a ir agregando los status de cada sku
status_disct = {}

#recorro cada sku de la lista y hago el request al sitio
for index, row in skus_df.iterrows():
    print(row[0])
    # get request al sitio
    response = requests.get(url + row[0],headers=headers)
    # verifico status del request
    if response.status_code != 200 :
        print("Connection problem: error " + str(response.status_code))
    else :
        print("Successful connection - " + str(index) )
        #valido si la url del request es redireccionada a la de busqueda sin resultados
        status_disct.update({row[0] : (response.url != (noResult + row[0]))})

#agrego columna a la lista de sku con el status- True: publicado - False:despublicado
status_pd = pd.DataFrame(status_disct.items(), columns=['sku', 'status'])
skus_df = skus_df.merge(status_pd, left_on='sku',right_on='sku', how='inner')

#hago el cruce con el skureport
skus_df["skuReport"] = skus_df.sku.isin(skuReport_df.SKU_ID)

#genero excel con el resultado
now = datetime.now()
skus_df.to_excel(now.strftime("%Y%m%d%H%M") + "_Catalyst_Despublicados_v2_.xlsx","data")

