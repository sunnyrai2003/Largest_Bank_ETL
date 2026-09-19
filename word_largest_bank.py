# Importing all the libraries..

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import lxml


# Required entities

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'

exchange_rate_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"

table_attribs = ["Name", "MC_USD_Billion"]

output_csv = "./Largest_banks_data.csv"

database_name = "Banks.db"

table_name = "Largest_banks"

log_file = "code_log.txt"


# Logging function

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing '''

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a") as f:
        f.write(timestamp + " : " + message + "\n")


# Extraction function

def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''

    page = requests.get(url).text

    data = BeautifulSoup(page, 'html.parser')

    tables = data.find_all('table')

    df = pd.DataFrame(columns=table_attribs)

    for row in tables[0].find_all('tr'):

        col = row.find_all('td')

        if len(col) != 0:

            name = col[1].text.strip()

            market_cap = col[2].text.strip()

            market_cap = float(market_cap)

            df1 = pd.DataFrame({
                'Name': [name],
                'MC_USD_Billion': [market_cap]
            })

            df = pd.concat([df, df1], ignore_index=True)

    return df


# First log entry

log_progress("Preliminaries complete. Initiating ETL process")


# Calling extract function

df = extract(url, table_attribs)

#print(df)


# Log extraction completion

log_progress("Data extraction complete. Initiating Transformation process")


# Calling extract function

df = extract(url, table_attribs)

# print(df)


# Log extraction completion

log_progress("Data extraction complete. Initiating Transformation process")


# Transformation function

def transform(df, exchange_rate_url):
    '''
    This function accesses the CSV file for exchange rate
    information and transforms the market capitalization
    values from USD to GBP, EUR and INR.
    '''

    exchange_rate_df = pd.read_csv(exchange_rate_url)

    exchange_rate = exchange_rate_df.set_index('Currency').to_dict()['Rate']

    gbp_rate = float(exchange_rate['GBP'])
    df['MC_GBP_Billion'] = [
        np.round(x * gbp_rate, 2)
        for x in df['MC_USD_Billion']
    ]

    eur_rate = float(exchange_rate['EUR'])
    df['MC_EUR_Billion'] = [
        np.round(x * eur_rate, 2)
        for x in df['MC_USD_Billion']
    ]

    inr_rate = float(exchange_rate['INR'])
    df['MC_INR_Billion'] = [
        np.round(x * inr_rate, 2)
        for x in df['MC_USD_Billion']
    ]

    return df


# Calling transform function

df = transform(df, exchange_rate_url)

print(df)


# Log transformation completion

log_progress("Data transformation complete. Initiating Loading process")

#print(df['MC_EUR_Billion'][4])


# Load transformed data to CSV

def load_to_csv(df, output_csv):
    '''
    This function saves the transformed dataframe
    to a CSV file.
    '''
    df.to_csv(output_csv, index=False)


# Calling load_to_csv function

load_to_csv(df, output_csv)

# Log CSV completion

log_progress("Data saved to CSV file")

def load_to_db(df, sql_connection, table_name):
    '''
    This function saves the transformed dataframe
    to an SQL database table.
    '''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


# Initiate SQLite3 connection

sql_connection = sqlite3.connect(database_name)

log_progress("SQL Connection initiated")


# Calling load_to_db function

load_to_db(df, sql_connection, table_name)

log_progress("Data loaded to Database as a table, Executing queries")

# Function to run SQL queries

def run_queries(query, sql_connection):
    '''
    This function runs the query on the SQLite database
    and prints the query along with its output.
    '''

    print("Query:")
    print(query)

    query_output = pd.read_sql(query, sql_connection)

    print(query_output)
    print()


 #Query 1: Print entire table

#query_statement = "SELECT * FROM Largest_banks"

#run_queries(query_statement, sql_connection)

# Query 2: Average market capitalization in GBP

query_statement = "SELECT AVG(MC_GBP_Billion) as AVG_MC_GBP_Billion FROM Largest_banks"

run_queries(query_statement, sql_connection)