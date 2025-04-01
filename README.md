# KBC Automated Tests

A Python-based framework for automated data validation testing between development and production environments in Keboola Connection.

## Usage

When developing in Keboola branches, as a reviewer you may want to automate some basic tests on some tables to ensure the integrity of the tables are to your expectation of the changes.  

This could be common in a project of medium complexity, with several end data products.  For example, imagine your project has 10 "gold layer" tables.  If a developer is making an upstream change, you want to know about what impacts it has across those 10 tables.  Especially if you do not have context about all 10, atleast you can explore or notify the owner of a changed table, in order to communicate the change.

This app has some basic tests, that can be expanded on, in order to write some of these tests to ensure integrity.  

Tests are written into a config file called `data_test_parametrics.csv` which you will configure.  

In your development branch, following the example above, you may have made a change upstream ("in the silver layer").  In your development branch, you will want to then run the orchestration/flow for everything downstream of that change (in this example, lets say it's just 5 gold layer tables downstream in that orchestration/flow).  So now in your development branch, there will be atleast 6 "development branch" tables, the 1 change in silver, and 5 tables from gold.  The application scans the entire branch for all development-branch-tables, then check if there are any tests for those tables in `data_test_parametrics`.  If found, those tests will execute.

Warning: A pitfall is that if in your development branch, you have not run a table that you want to test for, then it will not run that test.  Just because a test is listed in the `data_test_parametrics` table, does not mean it will execute.  The test will only execute in the presence of the table existing in the development branch. 



## Features

- Automated data validation tests between DEV and PROD environments
- Support for various test types:
  - Row count checks
  - Sum checks
  - Uniqueness checks
  - Input validation checks
- Streamlit-based web interface for test results visualization
- Configurable test parameters via CSV
- Snowflake integration for data validation

## Prerequisites

- Python 3.8+
- Snowflake account
- Keboola Connection account
- Streamlit

## Installation

1. Meant to be created as a data app within Keboola.  Either clone this repo, or point to this repo within Keboola.


2. Add secrets:
   - (if you are deeveloping locally Create a `.streamlit/secrets.toml` file with your credentials)
   - if in Keboola, add these into the Secrets.  Should be a read-only workspace that you set up for the Keboola project.
   ```toml
   [SNOWFLAKE_ACCOUNT]
   value = "your-account"

   [SNOWFLAKE_USER]
   value = "your-username"

   [SNOWFLAKE_PASSWORD]
   value = "your-password"

   [SNOWFLAKE_WAREHOUSE]
   value = "your-warehouse"

   ```

3. Configure your data_test_parametrics.csv and add it to input mapping.

Here is an example:

```
STORAGE_TABLE_ID,STORAGE_BUCKET_ID,TEST_NAME,SOURCE_BUCKET,SOURCE_TABLE,PARAMETER_1,PARAMETER_2,PARAMETER_3,PARAMETER_4
FCT_MONTH_END_CLOSE,out.c-base_zone_creation,check_row_count,n/a,n/a,n/a,n/a,n/a,n/a
FCT_MONTH_END_CLOSE,out.c-base_zone_creation,check_sum,n/a,n/a,AMOUNT,n/a,n/a,n/a
FCT_MONTH_END_CLOSE,out.c-base_zone_creation,check_uniqueness,n/a,n/a,MONTH_END_CLOSE_ID,n/a,n/a,n/a
FCT_BILLING_LINES,out.c-base_zone_creation,input_check_row_count,in.c-keboola-ex-db-mssql-1096073930,BillingLedgerDetail,n/a,n/a,n/a,n/a
FCT_BILLING_LINES,out.c-base_zone_creation,input_check_sum,in.c-keboola-ex-db-mssql-1096073930,BillingLedgerDetail,n/a,n/a,TotalAmount,TOTAL_AMOUNT_BILLED
```


### Available Tests

#### check_row_count
------

Checks the row count of the dev table specific, and the prod table. 

Configuration:
```
STORAGE_TABLE_ID,STORAGE_BUCKET_ID,TEST_NAME,SOURCE_BUCKET,SOURCE_TABLE,PARAMETER_1,PARAMETER_2,PARAMETER_3,PARAMETER_4
FCT_MONTH_END_CLOSE,out.c-base_zone_creation,check_row_count,n/a,n/a,n/a,n/a,n/a,n/a
```


#### check_sum
------

Checks the sum of a column of the dev table specific, and the prod table. 

Configuration:
```
STORAGE_TABLE_ID,STORAGE_BUCKET_ID,TEST_NAME,SOURCE_BUCKET,SOURCE_TABLE,PARAMETER_1,PARAMETER_2,PARAMETER_3,PARAMETER_4
FCT_MONTH_END_CLOSE,out.c-base_zone_creation,check_sum,n/a,n/a,AMOUNT,n/a,n/a,n/a
```



#### check_uniqueness
------

Checks the uniqueness of a column of the dev table specific, and the prod table. 

Configuration:
```
STORAGE_TABLE_ID,STORAGE_BUCKET_ID,TEST_NAME,SOURCE_BUCKET,SOURCE_TABLE,PARAMETER_1,PARAMETER_2,PARAMETER_3,PARAMETER_4
FCT_MONTH_END_CLOSE,out.c-base_zone_creation,check_uniqueness,n/a,n/a,MONTH_END_CLOSE_ID,n/a,n/a,n/a
```

PARAMETER_1 indicates the column that you are checking uniqueness for. 


#### input_check_row_count
------

For the dev table specified, select the "input mapping" of the table, and check the row count.

Useful to make sure that the transformation is matching the number of rows for input = output.  

The input table that will be used, will seek to find a dev version of that table.  Where the dev version does not exist, it will default to the production version of the table.  This is because, if you run a single transformation and running this test, the inputs that go into that transformation will be pulling from the production table, so a development table does not exist for those inputs (again, assuming that there was only the single transformation ran).

Configuration:
```
STORAGE_TABLE_ID,STORAGE_BUCKET_ID,TEST_NAME,SOURCE_BUCKET,SOURCE_TABLE,PARAMETER_1,PARAMETER_2,PARAMETER_3,PARAMETER_4
FCT_BILLING_LINES,out.c-base_zone_creation,input_check_row_count,in.c-keboola-ex-db-mssql-1096073930,BillingLedgerDetail,n/a,n/a,n/a,n/a
```



#### input_check_sum
------

For the dev table specified, select the "input mapping" of the table, and check the sum column.

Useful to make sure that the transformation is matching the sum of a column for input = output.  Used typically say, for a "invoices" table, you typically want the input \$ amount to match the output \$ amount.

Configuration:
```
STORAGE_TABLE_ID,STORAGE_BUCKET_ID,TEST_NAME,SOURCE_BUCKET,SOURCE_TABLE,PARAMETER_1,PARAMETER_2,PARAMETER_3,PARAMETER_4
FCT_BILLING_LINES,out.c-base_zone_creation,input_check_sum,in.c-keboola-ex-db-mssql-1096073930,BillingLedgerDetail,n/a,n/a,TotalAmount,TOTAL_AMOUNT_BILLED
```

PARAMETER_3 is the column name for the input.  (TotalAmount is for BillingLedgerDetail)

PARAMETER_4 is the column name for the output.  (TOTAL_AMOUNT_BILLED belongs to FCT_BILLING_LINES)


## Configure / Customize Your Own Tests

The tests above are the only tests available.  If you would like to customize your own tests, you will want to clone this repo and edit your own.  The steps are quite easy.

The queries are in the file `/queries/data_validation_queries.py`.  It is templatized there, so you just add your own queries there.

The project expects you to use the exact same schema for every SQL query.  If your SQL query does not follow that schema, the application will still run, and the query technically runs, but the results compiler will skip those results.

The name of the query in the `data_validation_queries.py` should match the name of the query in `data_test_parametrics.csv`.  