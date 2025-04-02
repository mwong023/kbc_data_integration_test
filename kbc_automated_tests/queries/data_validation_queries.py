"""
Data validation queries for Keboola tables

Note: The query names (first parameter in add_query) must match exactly with the TEST_NAME
values in data_test_parametrics.csv. This ensures a 1:1 mapping between test configurations
and their corresponding queries.

How to add new tests:
1. Copy an existing test block or the example below
2. Modify the query name (first parameter in add_query) to match your TEST_NAME in data_test_parametrics.csv
3. Update the SQL query to implement your validation logic
4. Ensure your query returns the same column structure:
   - TABLE_NAME: The name of the table being tested
   - TEST_NAME: The name of the test (must match add_query parameter)
   - COLUMN_NAME: The column being tested (use 'n/a' if not applicable)
   - ENVIRONMENT: Either 'DEV' or 'PROD'
   - VALUE: The result of your validation

Common patterns:
- Use UNION ALL to combine DEV and PROD results
- Use %(table_name)s for table references
- Use %(column_name)s for column references
- Use %(table_name_string)s and %(column_name_string)s for string literals
"""
from .base import QueryManager

class DataValidationQueries(QueryManager):
    """Collection of data validation queries"""
    
    def __init__(self):
        """Initialize data validation queries"""
        super().__init__()
        
        # Test 1: Compare row counts between dev and prod tables
        # Query name must match TEST_NAME in data_test_parametrics.csv
        self.add_query(
            "check_row_count",
            """
            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'check_row_count' as TEST_NAME,
                'n/a' as SOURCE_BUCKET,
                'n/a' as SOURCE_TABLE,
                'n/a' as PARAMETER_1,
                'n/a' as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'DEV' as ENVIRONMENT,
                COUNT(*) as VALUE
            FROM %(dev_table)s

            UNION ALL

            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'check_row_count' as TEST_NAME,
                'n/a' as SOURCE_BUCKET,
                'n/a' as SOURCE_TABLE,
                'n/a' as PARAMETER_1,
                'n/a' as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'PROD' as ENVIRONMENT,
                COUNT(*) as VALUE
            FROM %(prod_table)s
            """
        )
        
        # Test 2: Compare sum of a column between dev and prod tables
        # Query name must match TEST_NAME in data_test_parametrics.csv
        self.add_query(
            "check_sum",
            """
            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'check_sum' as TEST_NAME,
                'n/a' as SOURCE_BUCKET,
                'n/a' as SOURCE_TABLE,
                %(parameter_1_string)s as PARAMETER_1,
                'n/a' as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'DEV' as ENVIRONMENT,
                SUM(%(parameter_1_object)s) as VALUE
            FROM %(dev_table)s

            UNION ALL

            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'check_sum' as TEST_NAME,
                'n/a' as SOURCE_BUCKET,
                'n/a' as SOURCE_TABLE,
                %(parameter_1_string)s as PARAMETER_1,
                'n/a' as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'PROD' as ENVIRONMENT,
                SUM(%(parameter_1_object)s) as VALUE
            FROM %(prod_table)s
            """
        )
        
        # Test 3: Check uniqueness of a column (used for primary keys)
        # Query name must match TEST_NAME in data_test_parametrics.csv
        self.add_query(
            "check_uniqueness",
            """
            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'check_uniqueness' as TEST_NAME,
                'n/a' as SOURCE_BUCKET,
                'n/a' as SOURCE_TABLE,
                %(parameter_1_string)s as PARAMETER_1,
                'n/a' as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'DEV' as ENVIRONMENT,
                COUNT(DISTINCT %(parameter_1_object)s) as VALUE
            FROM %(dev_table)s

            UNION ALL

            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'check_uniqueness' as TEST_NAME,
                'n/a' as SOURCE_BUCKET,
                'n/a' as SOURCE_TABLE,
                %(parameter_1_string)s as PARAMETER_1,
                'n/a' as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'PROD' as ENVIRONMENT,
                COUNT(DISTINCT %(parameter_1_object)s) as VALUE
            FROM %(prod_table)s
            """
        )

        # Test 4: Check row count between source and target tables
        # Query name must match TEST_NAME in data_test_parametrics.csv
        self.add_query(
            "input_check_row_count",
            """
            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'input_check_row_count' as TEST_NAME,
                %(source_bucket_string)s as SOURCE_BUCKET,
                %(source_table_string)s as SOURCE_TABLE,
                'n/a' as PARAMETER_1,
                'n/a' as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'DEV' as ENVIRONMENT,
                COUNT(*) as VALUE
            FROM %(dev_table)s

            UNION ALL

            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'input_check_row_count' as TEST_NAME,
                %(source_bucket_string)s as SOURCE_BUCKET,
                %(source_table_string)s as SOURCE_TABLE,
                'n/a' as PARAMETER_1,
                'n/a' as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'PROD' as ENVIRONMENT,
                COUNT(*) as VALUE
            FROM %(source_bucket_object)s.%(source_table_object)s
            """
        )

        # Test 5: Check sum of a column between source and target tables
        self.add_query(
            "input_check_sum",
            """
            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'input_check_sum' as TEST_NAME,
                'n/a' as SOURCE_BUCKET,
                'n/a' as SOURCE_TABLE,
                %(parameter_1_string)s as PARAMETER_1,
                %(parameter_2_string)s as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'DEV' as ENVIRONMENT,
                SUM(%(parameter_2_object)s) as VALUE
            FROM %(dev_table)s

            UNION ALL

            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'input_check_sum' as TEST_NAME,
                'n/a' as SOURCE_BUCKET,
                'n/a' as SOURCE_TABLE,
                %(parameter_1_string)s as PARAMETER_1,
                %(parameter_2_string)s as PARAMETER_2,
                'n/a' as PARAMETER_3,
                'n/a' as PARAMETER_4,
                'PROD' as ENVIRONMENT,
                SUM(%(parameter_1_object)s) as VALUE
            FROM %(source_bucket_object)s.%(source_table_object)s
            """
        )
        

        # Example Test X: Check for NULL values and date ranges
        # This is an example of how to add a new test. Copy this block and modify as needed.
        # Demonstrates:
        # - Using multiple conditions in WHERE clause
        # - Working with dates
        # - Handling NULL values
        # - Using CASE statements for complex logic
        """
        self.add_query(
            "check_null_values_and_dates",
            \"""
            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'check_null_values_and_dates' as TEST_NAME,
                %(column_name_string)s as COLUMN_NAME,
                'DEV' as ENVIRONMENT,
                COUNT(CASE 
                    WHEN %(column_name)s IS NULL THEN 1
                    WHEN %(column_name)s < DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) THEN 1
                    ELSE NULL 
                END) as VALUE
            FROM %(dev_table)s
            WHERE %(column_name)s IS NULL 
               OR %(column_name)s < DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)

            UNION ALL

            SELECT 
                %(table_name_string)s as TABLE_NAME,
                'check_null_values_and_dates' as TEST_NAME,
                %(column_name_string)s as COLUMN_NAME,
                'PROD' as ENVIRONMENT,
                COUNT(CASE 
                    WHEN %(column_name)s IS NULL THEN 1
                    WHEN %(column_name)s < DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) THEN 1
                    ELSE NULL 
                END) as VALUE
            FROM %(prod_table)s
            WHERE %(column_name)s IS NULL 
               OR %(column_name)s < DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            \"""
        )
        """ 