"""
Test script for Snowflake connection and query execution
"""
from loguru import logger
from ..database.snowflake_client import SnowflakeClient

def test_snowflake_connection():
    """Test Snowflake connection and query execution"""
    logger.info("Starting Snowflake connection test")
    
    # Initialize Snowflake client
    client = SnowflakeClient()
    
    try:
        # Test connection
        client.connect()
        
        # Test query - replace this with your own query
        test_query = """
        SELECT 
            CURRENT_TIMESTAMP() as current_time,
            CURRENT_WAREHOUSE() as current_warehouse
        """
        
        # Execute query
        results = client.execute_query(test_query)
        
        if results:
            logger.info("Query executed successfully")
            logger.info(f"Columns: {results['columns']}")
            logger.info(f"Results: {results['results']}")
        else:
            logger.error("Query execution failed")
            
    except Exception as e:
        logger.error(f"Test failed: {e}")
    finally:
        # Always disconnect
        client.disconnect()

if __name__ == "__main__":
    test_snowflake_connection() 