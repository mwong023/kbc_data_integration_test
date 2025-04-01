"""
Integration test script for Keboola API functionality
"""
from loguru import logger
from ..api.keboola_client import KeboolaClient
from ..storage.bucket_manager import BucketManager

def test_api_integration():
    """Test all API integration functionality"""
    logger.info("Starting API integration tests")
    
    # Test KeboolaClient directly
    client = KeboolaClient()
    
    # Test listing branches
    logger.info("Testing branch listing...")
    branches = client.list_branches()
    logger.info(f"Found {len(branches)} branches")
    for branch in branches:
        logger.info(f"Branch: {branch}")
    
    # Test listing buckets
    logger.info("\nTesting bucket listing...")
    buckets = client.list_buckets()
    logger.info(f"Found {len(buckets)} buckets")
    for bucket in buckets:
        logger.info(f"Full bucket data: {bucket}")
    
    # Test BucketManager functionality
    logger.info("\nTesting BucketManager functionality...")
    bucket_manager = BucketManager()
    
    # Test with a specific branch ID (you'll need to replace this with a real branch ID)
    test_branch_id = "1191865"  # Replace with an actual branch ID from your environment
    
    # Test finding buckets by branch
    logger.info(f"\nTesting find_buckets_by_branch with branch ID: {test_branch_id}")
    branch_buckets = bucket_manager.find_buckets_by_branch(test_branch_id)
    logger.info(f"Found {len(branch_buckets)} buckets for branch {test_branch_id}")
    for bucket in branch_buckets:
        logger.info(f"Branch bucket ID: {bucket['id']}")
        
        # Test getting tables in bucket
        logger.info(f"\nTesting get_tables_in_bucket for bucket: {bucket['id']}")
        tables = bucket_manager.get_tables_in_bucket(bucket["id"])
        logger.info(f"Found {len(tables)} tables in bucket {bucket['id']}")
        for table in tables:
            logger.info(f"Table ID: {table['id']}")
        
        # Test production bucket ID conversion
        logger.info(f"\nTesting get_production_bucket_id for bucket: {bucket['id']}")
        prod_bucket = bucket_manager.get_production_bucket_id(bucket["id"], test_branch_id)
        logger.info(f"Production bucket ID: {prod_bucket}")
        
        # Test production bucket validation
        logger.info(f"\nTesting validate_production_bucket_exists for bucket: {bucket['id']}")
        exists = bucket_manager.validate_production_bucket_exists(bucket["id"], test_branch_id)
        logger.info(f"Production bucket exists: {exists}")

if __name__ == "__main__":
    test_api_integration() 