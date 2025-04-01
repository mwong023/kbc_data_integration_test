"""
Configuration settings for the Keboola Automated Tests Framework
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# Snowflake configuration
SNOWFLAKE_ACCOUNT = st.secrets["SNOWFLAKE_ACCOUNT"]
SNOWFLAKE_USER = st.secrets["SNOWFLAKE_USER"]
SNOWFLAKE_PASSWORD = st.secrets["SNOWFLAKE_PASSWORD"]
SNOWFLAKE_WAREHOUSE = st.secrets["SNOWFLAKE_WAREHOUSE"]

# Keboola configuration
KEBOOLA_API_TOKEN = os.getenv("KEBOOLA_API_TOKEN")
KEBOOLA_STORAGE_API_URL = os.getenv("KEBOOLA_STORAGE_API_URL", "https://connection.keboola.com")

# Test configuration
TEST_PARAMETRICS_FILE = DATA_DIR / "in" / "tables" / "data_test_parametrics.csv"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "kbc_automated_tests.log"

# Create necessary directories
os.makedirs(BASE_DIR / "logs", exist_ok=True) 