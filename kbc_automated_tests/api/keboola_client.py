"""
Keboola API client for handling API interactions
"""
import os
import requests
from typing import List, Dict, Optional
from loguru import logger
from kbc_automated_tests.config.config import KEBOOLA_API_TOKEN, KEBOOLA_STORAGE_API_URL

class KeboolaClient:
    """Client for interacting with Keboola API"""
    
    def __init__(self):
        """Initialize the Keboola client"""
        self.api_token = KEBOOLA_API_TOKEN
        self.base_url = KEBOOLA_STORAGE_API_URL
        self.headers = {
            "X-StorageApi-Token": self.api_token,
            "Content-Type": "application/json"
        }
        logger.info("Initialized Keboola API client")
    
    def list_branches(self) -> List[Dict]:
        """
        List all development branches
        
        Returns:
            List of branch dictionaries containing branch information
        """
        endpoint = f"{self.base_url}/v2/storage/dev-branches"
        logger.info("Fetching list of branches")
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching branches: {e}")
            raise
    
    def list_buckets(self) -> List[Dict]:
        """
        List all storage buckets
        
        Returns:
            List of bucket dictionaries containing bucket information
        """
        endpoint = f"{self.base_url}/v2/storage/buckets"
        logger.info("Fetching list of buckets")
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching buckets: {e}")
            raise
    
    def list_tables(self, bucket_id: str) -> List[Dict]:
        """
        List all tables in a bucket
        
        Args:
            bucket_id: ID of the bucket to list tables from
            
        Returns:
            List of table dictionaries containing table information
        """
        endpoint = f"{self.base_url}/v2/storage/buckets/{bucket_id}/tables"
        logger.info(f"Fetching tables from bucket: {bucket_id}")
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching tables: {e}")
            raise 