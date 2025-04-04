"""
Streamlit app for running data validation tests
"""
import streamlit as st
import os
from loguru import logger
from kbc_automated_tests.data_validator import DataValidator
from kbc_automated_tests.config.configuration import Configuration

# Configure Streamlit page
st.set_page_config(
    page_title="Keboola Data Validation Tests",
    page_icon="🔍",
    layout="wide"
)

def main():
    """Main Streamlit app function"""
    st.title("Keboola Data Validation Tests")
    
    # Initialize Keboola client
    from kbc_automated_tests.api.keboola_client import KeboolaClient
    
    # Configure logging to capture in Streamlit
    class StreamlitSink:
        def write(self, message):
            st.text(message)
            
    streamlit_sink = StreamlitSink()
    logger.add(streamlit_sink, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    
    try:
        # Get list of branches
        client = KeboolaClient()
        branches = client.list_branches()
        
        # Create selectbox for branches
        branch_options = [(branch['id'], f"{branch['name']} ({branch['id']})") for branch in branches]
        selected_branch = st.selectbox(
            "Select a branch",
            options=[id for id, _ in branch_options],
            format_func=lambda x: next(name for id, name in branch_options if id == x)
        )
        
        # Button to run tests
        if st.button("Run Validation Tests"):
            if selected_branch:
                with st.spinner("Running validation tests..."):
                    # Initialize validator
                    validator = DataValidator(str(selected_branch))
                    
                    # Run tests
                    results = validator.run_tests()
                    
                    # Display results
                    if not results.empty:
                        st.success("Tests completed successfully!")
                        st.dataframe(results)
                    else:
                        st.warning("No test results found")
            else:
                st.error("Please select a branch first")
                
    except Exception as e:
        st.error(f"Test execution failed: {str(e)}")
        
if __name__ == "__main__":
    main() 