"""
Storage bucket management module for Keboola Automated Tests
"""
from typing import List, Dict, Optional, Any
from loguru import logger
from ..api.keboola_client import KeboolaClient

class BucketManager:
    """Manages storage bucket operations and branch mapping"""
    
    def __init__(self):
        """Initialize the BucketManager"""
        self.client = KeboolaClient()
        logger.info("Initializing BucketManager")
    
    def find_buckets_by_branch(self, branch_id: str) -> List[Dict[str, Any]]:
        """
        Find all storage buckets that contain the given branch ID
        
        Args:
            branch_id: The branch ID to search for
            
        Returns:
            List of bucket dictionaries containing bucket information
        """
        logger.info(f"Searching for buckets containing branch ID: {branch_id}")
        buckets = self.client.list_buckets()
        matching_buckets = [
            bucket for bucket in buckets 
            if branch_id in bucket["id"]
        ]
        return matching_buckets
    
    def get_tables(self, bucket_id: str) -> List[Dict[str, Any]]:
        """
        Get all tables in a given storage bucket
        
        Args:
            bucket_id: ID of the storage bucket
            
        Returns:
            List of table dictionaries containing table information
        """
        logger.info(f"Fetching tables for bucket: {bucket_id}")
        return self.client.list_tables(bucket_id)
    
    def get_production_bucket_id(self, dev_bucket_id: str, branch_id: str) -> Optional[str]:
        """
        Convert a development bucket ID to its production equivalent
        
        Args:
            dev_bucket_id: ID of the development bucket
            branch_id: Branch ID to remove from the bucket ID
            
        Returns:
            Production bucket ID or None if conversion fails
        """
        logger.info(f"Converting dev bucket {dev_bucket_id} to production ID")
        if branch_id not in dev_bucket_id:
            logger.warning(f"Branch ID {branch_id} not found in bucket ID {dev_bucket_id}")
            return None
            
        # Find the position of the branch ID
        branch_pos = dev_bucket_id.find(branch_id)
        # Get the part before the branch ID
        prefix = dev_bucket_id[:branch_pos]
        # Get the part after the branch ID and its trailing dash
        suffix = dev_bucket_id[branch_pos + len(branch_id) + 1:]  # +1 to skip the trailing dash
        
        return f"{prefix}{suffix}"
    
    def validate_production_bucket_exists(self, dev_bucket_id: str, branch_id: str) -> bool:
        """
        Validate that the production bucket exists after converting from dev bucket
        
        Args:
            dev_bucket_id: ID of the development bucket
            branch_id: Branch ID to remove from the bucket ID
            
        Returns:
            True if production bucket exists, False otherwise
        """
        logger.info(f"Validating production bucket exists for dev bucket: {dev_bucket_id}")
        
        # Get the production bucket ID
        prod_bucket_id = self.get_production_bucket_id(dev_bucket_id, branch_id)
        if not prod_bucket_id:
            logger.warning(f"Could not convert dev bucket {dev_bucket_id} to production ID")
            return False
            
        # Check if the production bucket exists
        buckets = self.client.list_buckets()
        exists = any(bucket["id"] == prod_bucket_id for bucket in buckets)
        
        if exists:
            logger.info(f"Production bucket {prod_bucket_id} exists")
        else:
            logger.warning(f"Production bucket {prod_bucket_id} does not exist")
            
        return exists

    def bucket_exists(self, bucket_id: str) -> bool:
        """
        Check if a bucket exists
        
        Args:
            bucket_id: ID of the bucket to check
            
        Returns:
            True if bucket exists, False otherwise
        """
        logger.info(f"Checking if bucket exists: {bucket_id}")
        
        try:
            buckets = self.client.list_buckets()
            exists = any(bucket["id"] == bucket_id for bucket in buckets)
            
            if exists:
                logger.info(f"Bucket {bucket_id} exists")
            else:
                logger.info(f"Bucket {bucket_id} does not exist")
                
            return exists
        except Exception as e:
            logger.error(f"Error checking if bucket exists: {e}")
            return False 