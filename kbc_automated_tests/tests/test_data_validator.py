"""
Test script for DataValidator functionality
"""
from loguru import logger
from kbc_automated_tests.data_validator import DataValidator

def test_data_validator():
    """Test the DataValidator class functionality"""
    logger.info("Starting DataValidator test")
    
    # Initialize with specified branch ID
    validator = DataValidator("1191865")
    
    try:
        # Run tests and get results
        results = validator.run_tests()
        
        # Log results summary
        if not results.empty:
            logger.info(f"Test execution successful. Found {len(results)} results")
            logger.info(f"Results columns: {list(results.columns)}")
            logger.info(f"Number of unique tables tested: {results['TABLE_NAME'].nunique()}")
            logger.info(f"Number of unique tests run: {results['TEST_NAME'].nunique()}")
            
            # Log detailed results
            logger.info("\nDetailed Results:")
            logger.info(results.to_string())
        else:
            logger.warning("No test results found")
            
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise
        
if __name__ == "__main__":
    test_data_validator() 