import numpy as np
import pandas as pd


def compare_nps_categorical(df, nps_column, cat_column):
    '''
    Objetivo: comparar o NPS da avaliação escolhido condicional a variável categórica escolhida.
    Input:
    - df: dataset.
    - nps_column: nome da coluna de avaliação.
    - cat_column: nome da coluna de condição.   
    '''

    df_q1 = df.loc[df['mes'] <= '2022-03-01']
    df_q2 = df.loc[df['mes'] >= '2022-04-01']

    df_q1 = pd.pivot_table(data=df_q1.loc[df_q1[nps_column] != 'sem_avaliacao'], values='Id', index=cat_column, columns=nps_column, aggfunc='count', margins=True, margins_name='total_q1', fill_value=0).iloc[:-1].reset_index()
    
    df_q1['nps_q1'] = (df_q1['promotor'] - df_q1['detrator'])/df_q1['total_q1']

    df_q2 = pd.pivot_table(data=df_q2.loc[df_q2[nps_column] != 'sem_avaliacao'], values='Id', index=cat_column, columns=nps_column, aggfunc='count', margins=True, margins_name='total_q2', fill_value=0).iloc[:-1].reset_index()
    df_q2['nps_q2'] = (df_q2['promotor'] - df_q2['detrator'])/df_q2['total_q2']

    df_out = pd.merge(df_q1, df_q2[[cat_column, 'total_q2', 'nps_q2']], on=cat_column, how='left').round(2)
    return df_out[[cat_column, 'total_q1', 'total_q2', 'nps_q1', 'nps_q2']]