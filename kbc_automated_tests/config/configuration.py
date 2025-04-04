"""
Configuration management for the data validation framework
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict
from loguru import logger

class ConfigurationError(Exception):
    """Raised when there's an error in configuration"""
    pass

class Configuration:
    """Handles loading and accessing configuration"""
    
    def __init__(self, config_path: str = None):
        """Initialize configuration
        
        Args:
            config_path: Path to config file, defaults to config/config.yaml
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
            
        self.config = self._load_config(config_path)
        self._validate_config()
        
        # Convert paths to absolute paths
        if "paths" in self.config:
            data_root = os.environ.get("DATA_ROOT", "/data")  # Default to /data if not set
            for key, path in self.config["paths"].items():
                if not os.path.isabs(path):  # If path is not absolute
                    self.config["paths"][key] = os.path.join(data_root, path.lstrip("data/"))
        
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not config_path.exists():
            raise ConfigurationError(f"Config file not found: {config_path}")
            
        with open(config_path) as f:
            config = yaml.safe_load(f)
            
        # Replace environment variables
        return self._replace_env_vars(config)
        
    def _replace_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Replace ${ENV_VAR} with environment variable values"""
        if isinstance(config, dict):
            return {k: self._replace_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._replace_env_vars(v) for v in config]
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            env_var = config[2:-1]
            if env_var not in os.environ:
                raise ConfigurationError(f"Environment variable not found: {env_var}")
            return os.environ[env_var]
        return config
        
    def _validate_config(self):
        """Validate configuration"""
        required_sections = ["paths", "snowflake", "validation", "logging"]
        for section in required_sections:
            if section not in self.config:
                raise ConfigurationError(f"Missing required config section: {section}")
                
        # Validate paths exist
        for path_key, path_value in self.config["paths"].items():
            full_path = Path(path_value)
            if not full_path.exists():
                raise ConfigurationError(f"Path not found: {full_path}")
                
    def get(self, *keys: str, default: Any = None) -> Any:
        """Get configuration value by key path
        
        Args:
            *keys: Sequence of keys to traverse
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        value = self.config
        for key in keys:
            if not isinstance(value, dict):
                return default
            value = value.get(key, default)
            if value is None:
                return default
        return value 