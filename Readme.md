# World Largest Banks — ETL Project

## Project Overview

This project is an ETL (Extract, Transform, Load) pipeline developed
using Python to identify the top 10 largest banks in the world based
on market capitalization.

The market capitalization data is processed and converted from USD
into GBP, EUR, and INR using the provided exchange-rate data.

The final transformed data is stored in both CSV format and a
SQLite database for further analysis using SQL.


## ETL Workflow

### Extract
- Extract bank market capitalization data.
- Read exchange-rate data from CSV.

### Transform
- Clean the extracted data.
- Select the top 10 banks.
- Convert market capitalization from USD to GBP, EUR, and INR.

### Load
- Save the processed data into a CSV file.
- Store the processed data in a SQLite database.
- Use SQL queries to validate and analyze the data.



## Conclusion

This project demonstrates how a Data Engineer can build an end-to-end ETL pipeline to collect, transform, and store financial data.

The pipeline takes raw bank market-capitalization data and exchange-rate information, processes the data using Python and Pandas, converts the values into multiple currencies, and stores the final dataset in both CSV and SQLite database formats.

The project provided practical experience with the complete Extract → Transform → Load workflow and showed how Python, Pandas, SQL, and databases can work together to create a simple and reusable data pipeline.



###📌 Project Outcome

Raw Data → Extraction → Transformation → Currency Conversion → CSV + Database → SQL Analysis

This project forms a foundation for building more advanced Data Engineering pipelines using technologies such as PySpark, Airflow, Azure Data Factory, Databricks, and cloud data warehouses.
