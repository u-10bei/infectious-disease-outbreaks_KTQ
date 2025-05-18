import streamlit as st
import pandas as pd
import requests

@st.cache_data
def get_ido_data():
    
    DATA_URI = 'https://data.bodik.jp/api/3/action/datastore_search?resource_id=dd3b77f0-05c0-4899-892c-04909fd210e0&limit=1000'
    res_data = requests.get(DATA_URI)
    datas= res_data.json()
    ido_df = pd.DataFrame(datas["result"]["records"])
    ido_df.insert(6, 'date', pd.to_datetime(ido_df['年'].astype(str) +ido_df['週'].astype(str) + '1', format='%Y%W%w'))

    return ido_df

def get_diseases(df):   
    diseases = df.iloc[:, 7:]

    return diseases

def get_diseases_label(df):   
    diseases = get_diseases(df)
    diseases_label = diseases.columns.values

    return diseases_label

def get_current_data(df):
    current_data = df[df['_id'] == df['_id'].max()]

    return current_data

def get_max_disease(df):
    diseases = get_diseases(df)
    max_disease = diseases.apply(pd.to_numeric).idxmax(axis=1)

    return max_disease

def get_filtered_ido_df(column, key, df):
    filtered_df = df[(column >= key)].iloc[:, 4:].melt(id_vars=['date','年','週'], var_name='感染症', value_name='定点当たり患者数')
    filtered_df.insert(3, '年週', filtered_df['年'].astype(str) + '-' + filtered_df['週'].apply(lambda x: f"{x:02d}"))
    filtered_df['定点当たり患者数'] = filtered_df['定点当たり患者数'].apply(pd.to_numeric)

    return filtered_df

def fix_disease(df):
    df['定点当たり患者数'] = df['定点当たり患者数'].apply(pd.to_numeric)
