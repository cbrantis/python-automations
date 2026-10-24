import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import  xml.etree.ElementTree as ET
import requests 
import sqlite3

def log_progress(message):
    time_stamp_format = '%Y/%h/%d-%H:%M:%S'
    now = datetime.now()
    now_timestamp = now.strftime(time_stamp_format)
    with open (log_file,"a") as f:
        f.write(f"{message} : {now_timestamp} \n")



def extract(url, table_attribs):
    html_text = requests.get(url).text
    html_object = BeautifulSoup(html_text, 'html.parser')
    tables = html_object.find_all('tbody')
    banks_table = tables[0]
    rows = banks_table.find_all('tr')
    df_final = pd.DataFrame(columns = table_attribs)
    for row in rows:
        columns = row.find_all('td')
        if len(columns) != 0:
            data_dict = {'Name': columns[1].contents[2].text, 'MC_USD_Billion': float(columns[2].contents[0].text)}
            df_intermediate = pd.DataFrame(data_dict, index = [0])
            df_final = pd.concat([df_final,df_intermediate], ignore_index= 1)
    return df_final




def transform(df, csv_path):
    exchange_df = pd.read_csv(csv_path)
    exchange_dict = exchange_df.set_index('Currency').to_dict()['Rate']
    #for currency in ['GBP', 'EUR', 'INR']:
    for currency in list(exchange_dict.keys()):
        rate = float(exchange_dict[currency])
        df[f'MC_{currency}_Billion'] = (df['MC_USD_Billion']*rate).round(2)
    return df




def load_to_csv(df, output_path):
    df.to_csv(output_path)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection,if_exists='replace', index=False)





def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)




#Initiating global variables
URL = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs_ext = ['Name', 'MC_USD_Billion']
table_attribs_final = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
csv_path = 'Largest_banks_data.csv'
db_name = 'Banks.db'
table_name = 'Largest_banks'
log_file = 'code_log.txt'

log_progress('Preliminaries complete. Initiating ETL process')

#Start the exctraction process
df = extract(URL, table_attribs_ext)
log_progress('Data extraction complete. Initiating Transformation process')

#Start Transformation Process
df = transform(df, 'exchange_rate.csv')
log_progress('Data transformation complete. Initiating Loading process')

#Start Load Process
load_to_csv(df, csv_path)
log_progress('Data saved to CSV file')

#Start SQL connection
sql_connection = sqlite3.connect(db_name)
log_progress('SQL Connection initiated.')

#Load to db
load_to_db(df,sql_connection,table_name)
log_progress('Data loaded to Database as a table, Executing queries')

#Run query
run_query('SELECT * FROM Largest_banks', sql_connection)
run_query('SELECT AVG(MC_GBP_Billion) FROM Largest_banks', sql_connection)
run_query('SELECT Name from Largest_banks LIMIT 5', sql_connection)
log_progress('Process Complete')

#Close sql connection
sql_connection.close()
