import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3
import numpy as np 
import datetime


def extract(url, table_attribs):
    response = requests.get(url).text
    soup = BeautifulSoup(response,'html.parser')
    df = pd.DataFrame(columns = table_attribs)

    table_bodies = soup.find_all('tbody')
    rows = table_bodies[2].find_all('tr')

    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            if col[0].find('a') is not None and '—'not in col[2]:
                data_dict = {
                    'Country': col[0].a.contents[0],
                    'GDP_USD_millions': col[2].contents[0]
                }
                df1 = pd.DataFrame(data_dict, index= [0])
                df = pd.concat([df, df1], ignore_index = True)
    return df

def transform(df):

    return df

def load_to_csv(df, csv_path):

def load_to_db(df, sql_connection, table_name):

def run_query(query_statement, sql_connection):

def log_progress(message):


