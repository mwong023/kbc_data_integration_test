"""
Configuration manager for handling test configurations and matching
"""
import pandas as pd
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
        
    def _load_test_parametrics(self) -> pd.DataFrame:
        """Load test parametrics from CSV"""
        csv_path = self.config.get("paths", "test_parametrics")
        return pd.read_csv(csv_path)
        
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