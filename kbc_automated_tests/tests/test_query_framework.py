"""
Test script for running data validation tests
"""
from loguru import logger
import sys
from kbc_automated_tests.data_validator import DataValidator
from kbc_automated_tests.config.configuration import Configuration

def main():
    """Main function to run tests"""
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    
    # Load configuration
    config = Configuration()
    
    # Initialize data validator with branch ID
    branch_id = "1191865"  # Replace with your branch ID
    validator = DataValidator(branch_id, config)
    
    # Run tests and get results
    logger.info("Starting test execution...")
    results = validator.run_tests()
    
    # Display results
    if not results.empty:
        logger.info("\nTest Results DataFrame:")
        logger.info(results)
    else:
        logger.warning("No test results found")

if __name__ == "__main__":
    main() 