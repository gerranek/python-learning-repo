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

if upload: #could be also simple "if upload is not None:"
    st.write('File successsssfullllly uploaded.')

    df_upload = pd.read_csv(upload)
    df_clean = data_cleaner(df_upload)

    # average age
    av_age = round(df_clean['AGE'].mean())

    # most represented ethnicity
    ethnic_count = df_clean.groupby('ETHNIC')['ETHNIC'].count().reset_index(name='count')
    ethnic_count.sort_values('count', ascending=False, inplace=True)
    most_represented = ethnic_count.iloc[0]['ETHNIC']
    least_represented = ethnic_count.iloc[-1]['ETHNIC']
    #st.write(least_represented)

    # total number of children
    total_children = len(df_clean)

    # total number of each sex
    total_male = len(df_clean[df_clean['SEX'] == 'Male'])
    total_female = len(df_clean[df_clean['SEX'] == 'Female'])

    st.write(f'The average age is {av_age}.')
    st.write(f'The most represented ethnicity is {most_represented}, the least represented is {least_represented}.')
    st.write(f'The total number of children is {total_children}.')
    st.write(f'The total number of male children is {total_male}, and {total_female} for female.')
    st.write(f'The ratio is {total_male}/{total_female}.')

    # set values for min and max: 
    #lower_age_bound = 10
    #upper_age_bound = 20
    # or min and max from the dataframe: 
    lowest_age = int(df_clean['AGE'].min())
    highest_age = int(df_clean['AGE'].max())

    # sidebar:
    with st.sidebar: 
        age_boundaries = st.sidebar.slider(
            "Age range selection", 
            min_value=lowest_age, #min_value=0, 
            max_value=highest_age, #max_value=30, 
            value=[lowest_age, highest_age] #value=[0,30]
        )

        ethnicities = st.sidebar.multiselect(
            'Select ethnicities for data view:', 
            options=df_clean['ETHNIC'].unique(), 
            default=df_clean['ETHNIC'].unique()
        )

    ethnic_condition = df_clean['ETHNIC'].isin(ethnicities)

    age_condition = (df_clean['AGE'] >= age_boundaries[0]) & (df_clean['AGE'] <= age_boundaries[1])
    
    df_clean = df_clean[age_condition & ethnic_condition]

    st.dataframe(df_clean)

    age_bar_fig = age_bar(df_clean)
    st.plotly_chart(age_bar_fig)

    ethnic_pie_fig = ethnicity_pie(df_clean)
    st.plotly_chart(ethnic_pie_fig)
    