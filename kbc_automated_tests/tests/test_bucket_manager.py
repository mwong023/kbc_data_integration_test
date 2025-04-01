"""
Tests for the BucketManager class
"""
import pytest
from ..storage.bucket_manager import BucketManager

@pytest.fixture
def bucket_manager():
    """Create a BucketManager instance for testing"""
    return BucketManager()

def test_find_buckets_by_branch(bucket_manager):
    """Test finding buckets by branch ID"""
    branch_id = "test-branch"
    buckets = bucket_manager.find_buckets_by_branch(branch_id)
    assert isinstance(buckets, list)

def test_get_tables_in_bucket(bucket_manager):
    """Test getting tables from a bucket"""
    bucket_name = "test-bucket"
    tables = bucket_manager.get_tables_in_bucket(bucket_name)
    assert isinstance(tables, list)

def test_get_production_bucket_name(bucket_manager):
    """Test converting dev bucket name to production name"""
    dev_bucket = "dev-test-bucket"
    branch_id = "test-branch"
    prod_bucket = bucket_manager.get_production_bucket_name(dev_bucket, branch_id)
    assert prod_bucket is None or isinstance(prod_bucket, str)

def test_validate_bucket_exists(bucket_manager):
    """Test bucket validation"""
    bucket_name = "test-bucket"
    exists = bucket_manager.validate_bucket_exists(bucket_name)
    assert isinstance(exists, bool) 