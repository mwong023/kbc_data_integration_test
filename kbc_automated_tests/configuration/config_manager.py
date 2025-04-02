"""
Configuration manager for handling test configurations and matching
"""
import pandas as pd
import os
from typing import List, Tuple
from loguru import logger

from ..config.configuration import Configuration

class ConfigurationManager:
    """Handles loading and managing test configurations"""
    
    def __init__(self, config: Configuration):
        """Initialize configuration manager
        
        Args:
            config: Configuration object
        """
        self.config = config
        # Load test configurations
        self.test_parametrics = self._load_test_parametrics()
        
    def _validate_path(self, path: str) -> bool:
        """Validate if a path exists and is accessible
        
        Args:
            path: Path to validate
            
        Returns:
            bool: True if path exists and is accessible, False otherwise
        """
        if not path:
            logger.error("Path is empty")
            return False
            
        if not os.path.exists(path):
            logger.error(f"Path does not exist: {path}")
            return False
            
        if not os.path.isfile(path):
            logger.error(f"Path is not a file: {path}")
            return False
            
        if not os.access(path, os.R_OK):
            logger.error(f"Path is not readable: {path}")
            return False
            
        return True
        
    def _load_test_parametrics(self) -> pd.DataFrame:
        """Load test parametrics from CSV"""
        csv_path = self.config.get("paths", "test_parametrics")
        logger.info(f"Attempting to load test parametrics from: {csv_path}")
        
        # Validate path
        if not self._validate_path(csv_path):
            raise FileNotFoundError(f"Test parametrics file not found or not accessible: {csv_path}")
            
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Successfully loaded test parametrics with {len(df)} rows")
            logger.debug(f"Columns in test parametrics: {list(df.columns)}")
            return df
        except pd.errors.EmptyDataError:
            logger.error("Test parametrics file is empty")
            raise
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing test parametrics file: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading test parametrics: {e}")
            raise
        
    def find_matching_tests(self, prod_bucket: str, prod_table: str) -> List[Tuple[str, str]]:
        """Find all matching tests for production bucket and table
        
        Args:
            prod_bucket: Production bucket name
            prod_table: Production table name (full name including bucket)
            
        Returns:
            List of tuples (test_name, parameter_1) for each matching test
        """
        # Extract just the table ID from the full table name
        table_id = prod_table.split('.')[-1]
        
        # Find all matching rows in test parametrics
        matching_rows = self.test_parametrics[
            (self.test_parametrics['STORAGE_BUCKET_ID'] == prod_bucket) &
            (self.test_parametrics['STORAGE_TABLE_ID'] == table_id)
        ]
        
        if matching_rows.empty:
            logger.info(f"No tests found for {prod_bucket}.{table_id}")
            return []
            
        tests = []
        for _, row in matching_rows.iterrows():
            test_name = row['TEST_NAME']
            parameter_1 = row['PARAMETER_1']
            
            logger.info(f"Found test {test_name} for {prod_bucket}.{table_id}")
            tests.append((test_name, parameter_1))
            
        return tests 