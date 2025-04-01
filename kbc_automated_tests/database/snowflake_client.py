"""
Snowflake client for executing queries
"""
import os
from typing import List, Dict, Any
from loguru import logger
import snowflake.connector
import pandas as pd

class SnowflakeClient:
    """Client for executing Snowflake queries"""
    
    def __init__(self):
        """Initialize Snowflake client"""
        logger.info("Initializing Snowflake client")
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to Snowflake"""
        try:
            self.conn = snowflake.connector.connect(
                user=os.getenv('SNOWFLAKE_USER'),
                password=os.getenv('SNOWFLAKE_PASSWORD'),
                account=os.getenv('SNOWFLAKE_ACCOUNT'),
                warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
                database=os.getenv('SNOWFLAKE_DATABASE'),
                schema=os.getenv('SNOWFLAKE_SCHEMA')
            )
            self.cursor = self.conn.cursor()
            logger.info("Successfully connected to Snowflake")
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {e}")
            raise
            
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> pd.DataFrame:
        """Execute a query and return results as a pandas DataFrame
        
        Args:
            query: SQL query to execute
            params: Dictionary of parameters to bind to the query
            
        Returns:
            DataFrame containing query results
        """
        try:
            # Log the query and parameters for debugging
            logger.info("Executing query:")
            if params:
                # Replace parameters in query for logging
                actual_query = query
                for key, value in params.items():
                    actual_query = actual_query.replace(f"%({key})s", str(value))
                logger.info(actual_query)
                # Execute the query with parameters replaced
                self.cursor.execute(actual_query)
            else:
                logger.info(query)
                self.cursor.execute(query)
                
            # Fetch results directly into a pandas DataFrame
            df = self.cursor.fetch_pandas_all()
            logger.info(f"Query returned {len(df)} rows")
            
            # Log the results in a readable format
            logger.info("\nQuery Results:")
            logger.info(df.to_string())
            logger.info("\n")
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise
            
    def disconnect(self):
        """Disconnect from Snowflake"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logger.info("Disconnected from Snowflake") 