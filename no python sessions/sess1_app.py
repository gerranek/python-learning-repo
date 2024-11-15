import streamlit as st
import pandas as pd

def convert_df(df):
    return df.to_csv().encode("utf-8")

st.title('CIN benchmarking pipeline')

files = st.file_uploader(label='Please upload the CIN data:', 
                         accept_multiple_files=True)

dfs = {}

if files: # a failsafe the user has uploaded the files
    for f in files:
        df = pd.read_csv(f)
    
        key_string = f.name.split("/")[-1][:-17]
    
        dfs[key_string] = df
    
    #print(dfs)
    #print(dfs.keys())

    # order the tables so they sort in the rigth order
    dfs = {key:dfs[key] for key in sorted(dfs.keys())}
    #print(dfs)

    # and identify columns to merge on
    left_df = dfs['b1_children_in_need']
    merge_cols = list(left_df.columns[:10])

    new_col_names = [f'b1_children_in_need_{col}' if (not col in merge_cols) else col for col in dfs['b1_children_in_need'].columns]
    #print(new_col_names)
    left_df = left_df.set_axis(new_col_names, axis=1)

    for key, df in dfs.items():
        if (('headline_figures' not in key) &
            ('mid-year' not in key) &
            ('b1' not in key) &
            (key[0] != 'a')):

            df = df.set_axis([f'{key}_{col}' if (not col in merge_cols) else col for col in df.columns], axis=1)
        
            left_df = left_df.merge(df, how='left', on=merge_cols)
    #print(left_df.columns)

    wide_csv = convert_df(left_df)

    st.download_button(label='Click the fancy button to download', 
                       data=None, 
                       file_name='wide_benchmarking.csv', 
                       mime="text/csv")
    