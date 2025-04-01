"""
Test script to verify basic setup and configuration
"""
from loguru import logger
from ..config.config import (
    BASE_DIR,
    DATA_DIR,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_USER,
)

def test_basic_setup():
    """Test basic setup and configuration"""
    logger.info("Starting basic setup test")
    
    # Test directory structure
    assert BASE_DIR.exists(), "Base directory does not exist"
    assert DATA_DIR.exists(), "Data directory does not exist"
    
    # Test essential environment variables
    assert SNOWFLAKE_ACCOUNT is not None, "SNOWFLAKE_ACCOUNT is not set"
    assert SNOWFLAKE_USER is not None, "SNOWFLAKE_USER is not set"
    
    logger.info("Basic setup test completed successfully")

if __name__ == "__main__":
    test_basic_setup() 