import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3
import numpy as np 
from datetime import datetime


URL = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ['Country','GDP_USD_millions']
db_name = 'World_economies.db'
table_name = 'countries_by_GDP'
csv_path = '/home/project/ETL_GDP_DATA/Countries_by_GDP.csv'


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
    GDP_list = df['GDP_USD_millions'].tolist()
    #since the table has comma seprated data , it is stored as a string 
    #meaning we need to convert to numeric value first, that is why we converted
    #the series to list

    GDP_list = [float("".join(x.split(','))) for x in GDP_list]
    #lsit compreshension, split '1,234' as '1','234' and join as '1234' and 
    #convert to float as 1234.0
    
    GDP_list = [np.round(x/1000,2) for x in GDP_list] 
    df['GDP_USD_millions'] = GDP_list
    df  = df.rename(columns ={'GDP_USD_millions':'GDP_USD_billions'})
    return df

def load_to_csv(df, csv_path):
    df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists = 'replace', index = False)

def run_query(query_statement, sql_connection):
    print(query_statement)
    output =  pd.read_sql(query_statement, sql_connection)
    print(output)

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H-%M-%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open('/home/project/ETL_GDP_DATA/etl_project_log.txt', 'a') as f:
        f.write(timestamp + ' : ' + message + '\n')

log_progress('Preliminaries complete. Initiating ETL process')

df = extract(URL, table_attribs)

log_progress('Data extraction complete. Initiating Transformation process')

df = transform(df)

log_progress('Data transformation complete. Initiating loading process')\

load_to_csv(df, csv_path)

log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect(db_name)

log_progress('SQL Connection initiated.')

load_to_db(df, sql_connection, table_name)

log_progress('Data loaded to Database as table. Running the query')

query_statement = f"select * from {table_name} where GDP_USD_billions >= 100"
run_query(query_statement, sql_connection)

log_progress('Process Complete.')

sql_connection.close()




