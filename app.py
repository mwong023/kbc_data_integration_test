"""
Streamlit app for running data validation tests
"""
import streamlit as st
from loguru import logger
import sys
import io
import os
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    layout="wide",  # Use wide layout
    page_title="Keboola Data Validation Tests",
    page_icon="🔍"
)

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from the package
from kbc_automated_tests.api.keboola_client import KeboolaClient
from kbc_automated_tests.data_validator import DataValidator

# Configure logging to capture in Streamlit
def streamlit_sink(message):
    st.text(message)

# Add Streamlit sink to logger
logger.remove()  # Remove default handler
logger.add(streamlit_sink, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

def main():
    """Main Streamlit app function"""
    st.title("Keboola Data Validation Tests")
    
    # Initialize Keboola client
    try:
        client = KeboolaClient()
        logger.info("Successfully initialized Keboola client")
    except Exception as e:
        logger.error(f"Failed to initialize Keboola client: {e}")
        st.error("Failed to initialize Keboola client. Please check your configuration.")
        return
    
    # Get list of branches
    try:
        branches = client.list_branches()
        # Create a dictionary mapping display names to branch IDs
        branch_options = {f"{str(branch['id'])} - {branch['name']}": str(branch['id']) for branch in branches}
        branch_display_names = list(branch_options.keys())
        logger.info(f"Found {len(branch_display_names)} branches")
    except Exception as e:
        logger.error(f"Failed to fetch branches: {e}")
        st.error("Failed to fetch branches. Please check your configuration.")
        return
    
    # Branch selection dropdown
    selected_display = st.selectbox(
        "Select a branch to validate",
        branch_display_names,
        help="Choose a development branch to run validation tests against"
    )
    
    if selected_display:
        # Get the actual branch ID from the selected display name
        selected_branch = branch_options[selected_display]
        logger.info(f"Selected branch: {selected_display}")
        
        # Create a button to run tests
        if st.button("Run Validation Tests"):
            try:
                # Initialize validator with selected branch
                validator = DataValidator(str(selected_branch))  # Ensure branch ID is string
                logger.info("Initialized data validator")
                
                # Run tests and get results
                with st.spinner("Running validation tests..."):
                    results = validator.run_tests()
                    
                    if not results.empty:
                        logger.info(f"Test execution successful. Found {len(results)} results")
                        logger.info(f"Results columns: {list(results.columns)}")
                        logger.info(f"Number of unique tables tested: {results['TABLE_NAME'].nunique()}")
                        logger.info(f"Number of unique tests run: {results['TEST_NAME'].nunique()}")
                        
                        # Display results in a table with better formatting
                        st.subheader("Test Results")
                        st.dataframe(
                            results,
                            use_container_width=True,  # Use full width
                            hide_index=True,  # Hide the index column
                            column_config={
                                "VALUE": st.column_config.NumberColumn(
                                    "VALUE",
                                    format="%.2f"  # Format numbers with 2 decimal places
                                )
                            }
                        )
                        
                    else:
                        logger.warning("No test results found")
                        st.warning("No test results found for the selected branch.")
                        
            except Exception as e:
                logger.error(f"Test execution failed: {e}")
                st.error(f"Test execution failed: {str(e)}")

if __name__ == "__main__":
    main() 