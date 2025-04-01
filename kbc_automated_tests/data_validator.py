"""
Data validator for executing data validation tests in Keboola
This module handles the execution of data validation tests by:
1. Reading test configurations from CSV files
2. Finding matching tests for tables in development and production
3. Executing validation queries
4. Compiling results into a standardized format
"""
from typing import List, Dict, Optional
import pandas as pd
from loguru import logger

from .configuration.config_manager import ConfigurationManager
from .execution.query_executor import QueryExecutor
from .storage.bucket_manager import BucketManager
from .config.configuration import Configuration

class DataValidator:
    """Handles reading test configurations and executing data validation tests"""
    
    def __init__(self, branch_id: str, config: Optional[Configuration] = None):
        """Initialize data validator
        
        Args:
            branch_id: Branch ID to run tests for
            config: Configuration object, defaults to loading from default location
        
        Raises:
            ValueError: If branch_id is empty or None
        """
        if not branch_id:
            raise ValueError("branch_id cannot be empty")
            
        self.branch_id = branch_id
        self.config = config or Configuration()
        self.query_executor = QueryExecutor(self.config)
        self.config_manager = ConfigurationManager(self.config)
        self.bucket_manager = BucketManager()
        
    def _parse_prod_bucket(self, dev_bucket: str) -> str:
        """Parse production bucket name from development bucket
        
        Args:
            dev_bucket: Development bucket name
            
        Returns:
            Production bucket name
            
        Raises:
            ValueError: If dev_bucket is empty or None
        """
        if not dev_bucket:
            raise ValueError("dev_bucket cannot be empty")
            
        # Remove branch ID from dev bucket to get prod bucket
        return dev_bucket.replace(f"c-{self.branch_id}-", "c-")
        
    def _extract_table_name(self, full_table_id: str) -> str:
        """Extract just the table name from a full table ID
        
        Args:
            full_table_id: Full table ID including bucket
            
        Returns:
            Just the table name part
            
        Raises:
            ValueError: If full_table_id is empty or None
        """
        if not full_table_id:
            raise ValueError("full_table_id cannot be empty")
            
        return full_table_id.split('.')[-1]
        
    def _process_table(self, bucket_id: str, table: Dict) -> Optional[pd.DataFrame]:
        """Process a single table and run all applicable tests
        
        Args:
            bucket_id: ID of the bucket containing the table
            table: Dictionary containing table information
            
        Returns:
            DataFrame containing test results, or None if no tests found
            
        Raises:
            ValueError: If required parameters are missing
        """
        if not bucket_id or not table:
            raise ValueError("bucket_id and table are required")
            
        table_id = table['id']
        table_name = self._extract_table_name(table_id)
        prod_bucket = self._parse_prod_bucket(bucket_id)
        
        # Find all matching tests
        tests = self.config_manager.find_matching_tests(prod_bucket, table_id)
        if not tests:
            logger.info(f"No tests found for table {table_id}")
            return None
            
        # Construct table variables with proper quoting (for object references)
        dev_table = f'"{bucket_id}"."{table_name}"'
        prod_table = f'"{prod_bucket}"."{table_name}"'
        
        # Construct table variables with single quotes (for string literals)
        table_name_string = f"'{table_name}'"
        
        results = []
        for test_name, parameter_1 in tests:
            try:
                # Get test parameters from configuration
                test_config = self.config_manager.test_parametrics[
                    (self.config_manager.test_parametrics['TEST_NAME'] == test_name) &
                    (self.config_manager.test_parametrics['STORAGE_TABLE_ID'] == table_name) &
                    (self.config_manager.test_parametrics['STORAGE_BUCKET_ID'] == prod_bucket)
                ].iloc[0]
                
                # Handle source bucket/table references
                source_bucket_object = "NULL"
                source_bucket_string = "NULL"
                source_table_object = "NULL"
                source_table_string = "NULL"

                if pd.notna(test_config["SOURCE_BUCKET"]) and test_config["SOURCE_BUCKET"] != "n/a":
                    bucket_name = test_config["SOURCE_BUCKET"].split('.')[1]
                    dev_bucket_name = f"out.c-{self.branch_id}-{bucket_name}"
                    source_bucket = dev_bucket_name if self.bucket_manager.bucket_exists(dev_bucket_name) else test_config["SOURCE_BUCKET"]
                    source_bucket_object = f'"{source_bucket}"'
                    source_bucket_string = f"'{source_bucket}'"
                    
                    if pd.notna(test_config["SOURCE_TABLE"]) and test_config["SOURCE_TABLE"] != "n/a":
                        source_table_object = f'"{test_config["SOURCE_TABLE"]}"'
                        source_table_string = f"'{test_config['SOURCE_TABLE']}'"
                
                # Regular parameter handling
                parameter_1_object = f'"{test_config["PARAMETER_1"]}"' if pd.notna(test_config["PARAMETER_1"]) and test_config["PARAMETER_1"] != "n/a" else "NULL"
                parameter_2_object = f'"{test_config["PARAMETER_2"]}"' if pd.notna(test_config["PARAMETER_2"]) and test_config["PARAMETER_2"] != "n/a" else "NULL"
                parameter_3_object = f'"{test_config["PARAMETER_3"]}"' if pd.notna(test_config["PARAMETER_3"]) and test_config["PARAMETER_3"] != "n/a" else "NULL"
                parameter_4_object = f'"{test_config["PARAMETER_4"]}"' if pd.notna(test_config["PARAMETER_4"]) and test_config["PARAMETER_4"] != "n/a" else "NULL"
                
                parameter_1_string = f"'{test_config['PARAMETER_1']}'" if pd.notna(test_config["PARAMETER_1"]) and test_config["PARAMETER_1"] != "n/a" else "NULL"
                parameter_2_string = f"'{test_config['PARAMETER_2']}'" if pd.notna(test_config["PARAMETER_2"]) and test_config["PARAMETER_2"] != "n/a" else "NULL"
                parameter_3_string = f"'{test_config['PARAMETER_3']}'" if pd.notna(test_config["PARAMETER_3"]) and test_config["PARAMETER_3"] != "n/a" else "NULL"
                parameter_4_string = f"'{test_config['PARAMETER_4']}'" if pd.notna(test_config["PARAMETER_4"]) and test_config["PARAMETER_4"] != "n/a" else "NULL"
                
                # Execute test
                test_params = {
                    "dev_table": dev_table,
                    "prod_table": prod_table,
                    "table_name_string": table_name_string,
                    "source_bucket_object": source_bucket_object,
                    "source_bucket_string": source_bucket_string,
                    "source_table_object": source_table_object,
                    "source_table_string": source_table_string,
                    "parameter_1_object": parameter_1_object,
                    "parameter_2_object": parameter_2_object,
                    "parameter_3_object": parameter_3_object,
                    "parameter_4_object": parameter_4_object,
                    "parameter_1_string": parameter_1_string,
                    "parameter_2_string": parameter_2_string,
                    "parameter_3_string": parameter_3_string,
                    "parameter_4_string": parameter_4_string
                }
                
                result = self.query_executor.execute_tests(test_params, test_name)
                if not result.empty:
                    results.append(result)
                    
            except Exception as e:
                logger.error(f"Error executing test {test_name} for table {table_id}: {e}")
                continue
                
        if not results:
            return None
            
        return pd.concat(results, ignore_index=True)
        
    def run_tests(self) -> pd.DataFrame:
        """Run all applicable tests for the branch
        
        Returns:
            DataFrame containing all test results with standardized columns
            
        Raises:
            Exception: If connection to Snowflake fails
        """
        try:
            # Connect to Snowflake
            self.query_executor.connect()
            
            # List to store all results
            all_results = []
            
            # Get all dev buckets for branch
            dev_buckets = self.bucket_manager.find_buckets_by_branch(self.branch_id)
            if not dev_buckets:
                logger.warning(f"No development buckets found for branch {self.branch_id}")
                return pd.DataFrame()
                
            for dev_bucket in dev_buckets:
                bucket_id = dev_bucket['id']
                
                try:
                    # Get tables for this bucket
                    tables = self.bucket_manager.get_tables(bucket_id)
                    if not tables:
                        logger.info(f"No tables found in bucket {bucket_id}")
                        continue
                        
                    for table in tables:
                        result = self._process_table(bucket_id, table)
                        if result is not None:
                            all_results.append(result)
                            
                except Exception as e:
                    logger.error(f"Error processing bucket {bucket_id}: {e}")
                    continue
                    
            if not all_results:
                logger.warning("No test results found")
                return pd.DataFrame()
                
            # Compile all results
            return self.query_executor.compile_results(all_results)
                    
        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
            raise
        finally:
            self.query_executor.disconnect() 