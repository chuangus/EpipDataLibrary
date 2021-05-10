# -*- coding: utf-8 -*-
"""
Created on Tue May  4 16:35:48 2021

@author: Angus
"""


import pandas as pd
import numpy as np



pages = np.arange(1, 20)
df2= pd.DataFrame()


### gathers data W.T to listed IPO performance
for page in pages:
    
    page="http://www.aastocks.com/en/stocks/market/ipo/listedipo.aspx?s=3&o=0&page=" + str (page)

    dfs = pd.read_html(page)
    df = dfs [16]
    df = df [:-3]
    df = df.iloc [:,1:]
    df2 = df2.append(df)

df = df2

#data cleaning

df2 = df ['Name▼ / Code▼']
df2 = df2.map(lambda x: x.rstrip('Sink Below Listing Price'))
df_code = df2.map(lambda x: x[-7:])
df_name =  df2.map(lambda x: x[:-8])

df ['Name▼ / Code▼'] = df_code
df.insert(0, 'Name', df_name)
df = df.rename(columns = {'Name▼ / Code▼':'Code'})


def zsplit (column,df, colnumber):
    df2 = df [column]
    df4 = pd.DataFrame()
    for a in df2:
        try:
            a = str(a)
            df3 = a.split ('-') 
            df5 = pd.DataFrame({'Lower '+column: [df3[0]],'Upper ' + column :[df3 [1]]})
            df4 = df4.append(df5)
        except IndexError:
            a = str(a)
            df6 = a
            df6 = pd.DataFrame({'Lower ' + column: [df6],'Upper ' + column :'nan'})
            df4 = df4.append(df6)
        except AttributeError:
            a = str(a)
            df6 = a
            df6 = pd.DataFrame({'Lower ' + column: [df6],'Upper ' + column :'nan'})
            df4 = df4.append(df6)
    df4 = df4.reset_index()
    df5 = df4 ['Upper ' + column]
    df6 = df4 ['Lower ' + column]
    
    df [column] = df6
    df = df.rename(columns = {column:'Lower ' + column})
    df.insert(colnumber,'Upper ' + column, value = df5)
    return df

df = zsplit('Market Cap(B)',df, 5)
df = zsplit('Offer Price',df, 7)

df.to_csv('IPO.csv', index= False)