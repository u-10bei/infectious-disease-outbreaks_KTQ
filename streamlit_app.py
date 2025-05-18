import streamlit as st
import pandas as pd
import math
import datas as dt

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='北九州市の感染症発生動向（定点報告）',
    page_icon=':hospital:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

ido_df = dt.get_ido_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :hospital: 北九州市の感染症発生動向（定点報告）

[北九州市オープンデータ](https://odcs.bodik.jp/401005/)のウェブサイトから  
[感染症発生動向](https://data.bodik.jp/dataset/401005_kansensyohasseidoko_teitenhokoku/resource/dd3b77f0-05c0-4899-892c-04909fd210e0)を無料で閲覧できます。
'''

# Add some spacing
''

# 感染症のリスト
diseases = dt.get_diseases_label(ido_df)

# 最新データ
current_data = dt.get_current_data(ido_df)

# 最新データのうち最も多い感染症
max_disease = dt.get_max_disease(current_data)

''

# グラフの選択
selected_type = st.selectbox(
    'どのグラフを表示したいですか？',
    ('過去１年間の状況', '去年と今年の比較', '過去３年の比較')
)

# 感染症の選択
if selected_type == '過去１年間の状況':
    selected_disease = st.multiselect(
        'どの感染症を確認したいですか？',
        diseases,
        max_disease,
    )
else:
    selected_disease = st.selectbox(
        'どの感染症を確認したいですか？',
        diseases,
    )    

''
''

# Filter the data
if selected_type == '過去１年間の状況':
    filtered_column = ido_df['date']
    filtered_key = pd.to_datetime((current_data.iloc[0]['年'] - 1).astype(str) + current_data.iloc[0]['週'].astype(str) + "1", format='%Y%W%w')  
elif selected_type == '去年と今年の比較':
    filtered_column = ido_df['年']
    filtered_key = ido_df['年'].max() - 1
elif selected_type == '過去３年の比較':
    filtered_column = ido_df['年']        
    filtered_key = ido_df['年'].max() - 2

filtered_ido_df = dt.get_filtered_ido_df(filtered_column, 
                                      filtered_key, 
                                      ido_df)

st.header(selected_type, divider='gray')

''
# グラフの描画
if selected_type == '過去１年間の状況':
    filtered_ido_df = filtered_ido_df[
        (filtered_ido_df['感染症'].isin(selected_disease))]
    st.line_chart(
        filtered_ido_df,
        x='年週',
        y='定点当たり患者数',
        color='感染症',
    )
else:
    filtered_ido_df = filtered_ido_df[
        (filtered_ido_df['感染症'] == selected_disease)]
    filtered_ido_df['年'] = filtered_ido_df['年'].astype(str)
    st.line_chart(
        filtered_ido_df,
        x='週',
        y='定点当たり患者数',
        color='年',    
    )

''
''

current_disease = current_data.iloc[:, 4:].melt(id_vars=['date','年','週'], var_name='感染症', value_name='定点当たり患者数')
dt.fix_disease(current_disease)

lastweek_key = pd.to_datetime(current_data.iloc[0]['年'].astype(str) + (current_data.iloc[0]['週'] - 1).astype(str) + "1", format='%Y%W%w')
lastweek_disease = ido_df[(ido_df['date'] == lastweek_key)].iloc[:, 4:].melt(id_vars=['date','年','週'], var_name='感染症', value_name='定点当たり患者数')
dt.fix_disease(lastweek_disease)

lastyear_key = pd.to_datetime((current_data.iloc[0]['年'] - 1).astype(str) + current_data.iloc[0]['週'].astype(str) + "1", format='%Y%W%w')
lastyear_disease = ido_df[(ido_df['date'] == lastyear_key)].iloc[:, 4:].melt(id_vars=['date','年','週'], var_name='感染症', value_name='定点当たり患者数')
lastyear_disease['定点当たり患者数'] = lastyear_disease['定点当たり患者数'].apply(pd.to_numeric)

st.header('今週の感染症発生動向', divider='gray')

''

cols = st.columns(3)

for i, types in enumerate(diseases):
    col = cols[i % len(cols)]
    with col:
        current_number = current_disease[current_disease['感染症'] == types]['定点当たり患者数'].iat[0]
        lastweek_number = lastweek_disease[lastweek_disease['感染症'] == types]['定点当たり患者数'].iat[0]
        lastyear_number = lastyear_disease[lastyear_disease['感染症'] == types]['定点当たり患者数'].iat[0]

        if math.isnan(lastweek_number):
            lw_growth = 'n/a'
            lw_delta_color = 'off'
        elif current_number == lastweek_number:
            lw_growth = 0
            lw_delta_color = 'off'            
        else:
            lw_growth = f'{current_number - lastweek_number:,.2f}'
            lw_delta_color = 'normal'

        if math.isnan(lastyear_number):
            ly_growth = 'n/a'
            ly_delta_color = 'off'
        elif current_number == lastyear_number:
            ly_growth = 0
            ly_delta_color = 'off'       
        else:
            ly_growth = f'{current_number - lastyear_number:,.2f}'
            ly_delta_color = 'normal'

        with st.container(border=True):
            st.metric(
                label=f'{types}',
                value=f'{current_number:,.2f}',
            )
            st.metric(
                label='（先週）',
                value=f'{lastweek_number:,.2f}',
                delta=lw_growth,
                delta_color=lw_delta_color
            )               
            st.metric(
                label='（昨年同週）',
                value=f'{lastyear_number:,.2f}',
                delta=ly_growth,
                delta_color=ly_delta_color
            )
