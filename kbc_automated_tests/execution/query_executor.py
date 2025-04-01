"""
Query executor for handling query execution and result compilation
"""
import os
import pandas as pd
from typing import Dict, List
from loguru import logger

from ..database.snowflake_client import SnowflakeClient
from ..queries.data_validation_queries import DataValidationQueries
from ..config.configuration import Configuration

class QueryExecutor:
    """Handles query execution and result compilation"""
    
    def __init__(self, config: Configuration):
        """Initialize query executor
        
        Args:
            config: Configuration object
        """
        self.config = config
        
        # Set environment variables for Snowflake connection
        os.environ['SNOWFLAKE_USER'] = config.get("snowflake", "username")
        os.environ['SNOWFLAKE_PASSWORD'] = config.get("snowflake", "password")
        os.environ['SNOWFLAKE_ACCOUNT'] = config.get("snowflake", "account")
        os.environ['SNOWFLAKE_WAREHOUSE'] = config.get("snowflake", "warehouse")
        
        # Initialize Snowflake client
        self.snowflake = SnowflakeClient()
        self.queries = DataValidationQueries()
        
    def execute_tests(self, test_params: Dict[str, str], test_name: str) -> pd.DataFrame:
        """Execute a test query and return results
        
        Args:
            test_params: Parameters for the query
            test_name: Name of the test to execute
            
        Returns:
            DataFrame containing test results
        """
        try:
            result = self.snowflake.execute_query(
                self.queries.get_query(test_name),
                test_params
            )
            
            # If result is empty, return empty DataFrame with required columns
            if result.empty:
                required_columns = self.config.get("validation", "required_columns")
                return pd.DataFrame(columns=required_columns)
            
            # Verify result has correct columns
            required_columns = self.config.get("validation", "required_columns")
            if list(result.columns) != required_columns:
                logger.error(f"Test {test_name} returned incorrect columns: {list(result.columns)}")
                return pd.DataFrame(columns=required_columns)
                
            return result
            
        except Exception as e:
            logger.error(f"Error executing test {test_name}: {str(e)}")
            required_columns = self.config.get("validation", "required_columns")
            return pd.DataFrame(columns=required_columns)
        
    def compile_results(self, results: List[pd.DataFrame]) -> pd.DataFrame:
        """Compile multiple test results into a single DataFrame
        
        Args:
            results: List of result DataFrames
            
        Returns:
            Combined DataFrame with all results
        """
        if not results:
            required_columns = self.config.get("validation", "required_columns")
            return pd.DataFrame(columns=required_columns)
            
        final_results = pd.concat(results, ignore_index=True)
        logger.info(f"Combined {len(results)} test results into final DataFrame")
        return final_results
        
    def connect(self):
        """Connect to Snowflake"""
        self.snowflake.connect()
        
    def disconnect(self):
        """Disconnect from Snowflake"""
        self.snowflake.disconnect() 