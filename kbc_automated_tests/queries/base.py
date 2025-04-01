"""
Base class for query management
"""
from typing import Dict, Any, Optional
from loguru import logger

class QueryManager:
    """Base class for managing and executing queries"""
    
    def __init__(self):
        """Initialize the query manager"""
        self.queries: Dict[str, str] = {}
        logger.info("Initializing QueryManager")
    
    def add_query(self, query_id: str, query_template: str) -> None:
        """
        Add a query template to the manager
        
        Args:
            query_id: Unique identifier for the query
            query_template: SQL query template with placeholders
        """
        self.queries[query_id] = query_template
        logger.info(f"Added query template: {query_id}")
    
    def get_query(self, query_id: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Get a query with parameters replaced
        
        Args:
            query_id: ID of the query to retrieve
            params: Dictionary of parameters to replace in the query
            
        Returns:
            Formatted query string
        """
        if query_id not in self.queries:
            raise KeyError(f"Query {query_id} not found")
            
        query = self.queries[query_id]
        if params:
            try:
                return query.format(**params)
            except KeyError as e:
                raise KeyError(f"Missing required parameter: {e}")
                
        return query 