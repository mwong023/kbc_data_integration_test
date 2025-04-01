"""
Test queries for data validation
"""
from .base import QueryManager

class TestQueries(QueryManager):
    """Collection of test queries"""
    
    def __init__(self):
        """Initialize test queries"""
        super().__init__()
        
        # Example: Query to count rows in a table
        self.add_query(
            "count_rows",
            """
            SELECT COUNT(*) as row_count
            FROM {table_name}
            """
        )
        
        # Example: Query to check for null values in a column
        self.add_query(
            "check_null_values",
            """
            SELECT 
                COUNT(*) as total_rows,
                SUM(CASE WHEN {column_name} IS NULL THEN 1 ELSE 0 END) as null_count
            FROM {table_name}
            """
        )
        
        # Example: Query to check for duplicate values
        self.add_query(
            "check_duplicates",
            """
            SELECT 
                {column_name},
                COUNT(*) as occurrence_count
            FROM {table_name}
            GROUP BY {column_name}
            HAVING COUNT(*) > 1
            """
        )
        
        # Example: Query to check value ranges
        self.add_query(
            "check_value_range",
            """
            SELECT 
                COUNT(*) as out_of_range_count
            FROM {table_name}
            WHERE {column_name} < {min_value} 
               OR {column_name} > {max_value}
            """
        )
        
        # Add more queries here as needed
        # Example:
        # self.add_query(
        #     "check_null_values",
        #     """
        #     SELECT COUNT(*) as null_count
        #     FROM {table_name}
        #     WHERE {column_name} IS NULL
        #     """
        # ) 