# build instructions

The purpose of this application is to build a dynamic and automated data testing framework for Keboola.

The application will be built in Python + Streamlit.

The flow of the application will be this:

1. Streamlit has a dropdown that has the list of branch id's and branch names
2. User will select a branch
3. The rest of the application will do the following in order:
 - based on the branch id, do a string search in every storage bucket to see if the id is ilike anywhere in the storage bucket name.  This searches for any buckets that were created in the dev branch, and is the dev version of that bucket.
 - after finding all the buckets with a matched branch id, then list all the tables under that storage bucket name.  these are all the dev versions of the table under the dev storage bucket. 
 - remove the branch id from the storage bucket names.  by removing the branch id from the storage bucket name, the result is the identifier of the production storage bucket name.
 - search for the matching production bucket and table names, in data/in/tables/data_test_parametrics.csv table.  
 - if there is a test for the listed table, then based on the test_id in the data_test_parametrics table, it will execute queries and save the results in a dataframe
 - before executing the above queries, we will need to establish a connection to a Snowflake workspace.  If possible, lets establish the Snowflake workspace earlier to open the session, and keep the connection open until the application closes. 
 - after executing all the queries which are tests, all as dataframes, compile it all together.  each of these tests will have a standard schema so they just need to be unioned or inserted together. 
 - display the results in streamlit