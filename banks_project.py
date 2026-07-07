from datetime import datetime
url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ['Name', 'MC_USD_Billion']
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3
import numpy as np
csv_path ="./exchange_rate.csv" 
output_path = './Largest_banks_data.csv'
sql_connection = sqlite3.connect('Banks.db')
table_name = ""
# Code for ETL operations on Country-GDP data

# Importing the required libraries

def log_progress(message):
    now = datetime.now()
    timestamp = now.strftime('%Y-%h-%d-%H:%M:%S')
    with open("code_log.txt", "a") as f:
        f.write(f"{timestamp} : {message} \n")
    
    
def extract(url, table_attribs):
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {
                "Name": col[1].text.strip(),
                "MC_USD_Billion": col[2].text.strip()
            }
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)
       
    return df

def transform(df, csv_path):
    
    exchange_df = pd.read_csv(csv_path)
    exchange_rate = exchange_df.set_index('Currency').to_dict()['Rate']
    
    df['MC_USD_Billion'] = df['MC_USD_Billion'].astype(float)
    # GBP RATE
    gbp_rate = float(exchange_rate['GBP'])

    df['MC_GBP_Billion'] = [np.round(x * gbp_rate, 2) for x in 
    df['MC_USD_Billion']]
    
    # EUR RATE
    Eur_rate = float(exchange_rate['EUR'])

    df['MC_EUR_Billion'] = [np.round(x * Eur_rate, 2) for x in 
    df['MC_USD_Billion']]
    
    # INR RATE
    INR_rate = float(exchange_rate['INR'])

    df['MC_INR_Billion'] = [np.round(x * INR_rate, 2) for x 
    in df['MC_USD_Billion']]
    
    return df
    
    

  

def load_to_csv(tf, output_path):
    df.to_csv(output_path , index=False)  



def load_to_db(tf, sql_connection, table_name):
    df.to_sql(table_name , sql_connection ,if_exists = 'replace' , index=False) 
 

      
def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)




# function call 


# extract 

df = extract(url , table_attribs)
# print(df)
log_progress("Data extraction complete. Initiating Transformation process")

# Transform


tf = transform(df , csv_path)
# print(tf)
# print(tf['MC_EUR_Billion'][4])
# print
log_progress("Data transformation complete. Initiating Loading process")

# Loading to csv

csv_data =  load_to_csv(tf ,output_path)
# print("data saved to csv file")
log_progress("Data saved to CSV file")


# Load to DB

load_to_db(tf,sql_connection ,"Largest_Banks" )
log_progress("SQL Connection initiated")
# print("sql connection established") 


# Querying database

query_statement = "SELECT * FROM Largest_Banks"

query_statement2 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"

query_statement3 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks LIMIT 5"


run_query(query_statement, sql_connection)
run_query(query_statement2, sql_connection)

run_query(query_statement3, sql_connection)
log_progress("Data loaded to Database as a table, Executing queries")




log_progress("Process Complete")

sql_connection.close()
log_progress("Server Connection closed")


