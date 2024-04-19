import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# functions:
# utilities:
def data_cleaner(df):
    # TODO map SEX to male/female
    # TODO calculate ages - change DOB to datetime
    # TODO drop excess columns

    '''
    cleans 903 header and adss age column

    arguments:
    df -> DataFrame of 903 header data to be cleaned

    returns:
    df -> DataFrame of 903 data with SEX correctly mapped and AGE column added
    '''

    df['SEX'] = df['SEX'].map({1:'Male',
                               2:'Female'})
    
    df['DOB'] = pd.to_datetime(df['DOB'], format="%d/%m/%Y", errors='coerce')
    df['AGE'] = pd.to_datetime('today').normalize() - df['DOB']
    df['AGE'] = (df['AGE'] / np.timedelta64(1, 'Y')).astype('int')

    #one way to drop certain columns: df.drop()
    df = df[['SEX', 'AGE', 'ETHNIC']]

    return df #this needs to be there otherwise you don't get anything

# plotting functions:
def age_bar(df):
    fig = px.histogram(df, 
                       x='SEX', 
                       title='Breakdown by gender of 903 data', 
                       labels={'SEX':'Sex of children'})
                       #color='ETHNIC'

    return fig

def ethnicity_pie(df):
    ethnic_count = df.groupby('ETHNIC')['ETHNIC'].count().reset_index(name='count')
    st.dataframe(ethnic_count)

    fig = px.pie(ethnic_count, 
                 values='count', 
                 names='ETHNIC')

    return fig

# the app:
st.title('903 header analysis tool')

upload = st.file_uploader('Please upload 903 header as a .csv')

if upload is not None: #could be also simple "if upload:"
    st.write('File successsssfullllly uploaded.')

    df_upload = pd.read_csv(upload)
    df_clean = data_cleaner(df_upload)

    st.dataframe(df_clean)

    age_bar_fig = age_bar(df_clean)
    st.plotly_chart(age_bar_fig)

    ethnic_pie_fig = ethnicity_pie(df_clean)
    st.plotly_chart(ethnic_pie_fig)
    