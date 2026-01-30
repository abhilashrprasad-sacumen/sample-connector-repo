# src/config_loader.py

"""
Configuration Loader for Qualys CloudView Connector
=====================================================

Loads configuration from YAML file.
Supports environment variable overrides for sensitive data.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QualysConfig:
    """Qualys API configuration."""
    base_url: str
    username: str
    password: str


@dataclass
class APIConfig:
    """API endpoint configuration."""
    endpoint: str
    default_page_size: int
    timeout_seconds: int


@dataclass
class Config:
    """Complete application configuration."""
    qualys: QualysConfig
    api: APIConfig


def find_config_file() -> Optional[Path]:
    """
    Find the config file in common locations.
    
    Search order:
    1. Current directory
    2. Parent directory (project root)
    3. src directory
    
    Returns:
        Path to config file or None if not found
    """
    search_paths = [
        Path.cwd() / "config.yaml",
        Path.cwd() / "config.yml",
        Path.cwd().parent / "config.yaml",
        Path.cwd().parent / "config.yml",
        Path(__file__).parent.parent / "config.yaml",
        Path(__file__).parent.parent / "config.yml",
    ]
    
    for path in search_paths:
        if path.exists():
            logger.info(f"Found config file: {path}")
            return path
    
    return None


def load_yaml_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Optional path to config file. If None, searches common locations.
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file not found
    """
    if config_path is None:
        config_path = find_config_file()
    
    if config_path is None or not config_path.exists():
        raise FileNotFoundError(
            "Configuration file not found. "
            "Please copy config.example.yaml to config.yaml and fill in your credentials."
        )
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def load_config(config_path: Optional[Path] = None) -> Config:
    """
    Load configuration with environment variable overrides.
    
    Environment variables take precedence over config file values:
    - QUALYS_BASE_URL: Overrides qualys.base_url
    - QUALYS_USERNAME: Overrides qualys.username
    - QUALYS_PASSWORD: Overrides qualys.password
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        Config object with all settings
    """
    yaml_config = load_yaml_config(config_path)
    
    # Extract Qualys config with environment variable overrides
    qualys_section = yaml_config.get('qualys', {})
    qualys_config = QualysConfig(
        base_url=os.getenv('QUALYS_BASE_URL', qualys_section.get('base_url', '')),
        username=os.getenv('QUALYS_USERNAME', qualys_section.get('username', '')),
        password=os.getenv('QUALYS_PASSWORD', qualys_section.get('password', '')),
    )
    
    # Validate credentials
    if not qualys_config.username or qualys_config.username == 'your_qualys_username':
        logger.warning("Qualys username not configured. Please update config.yaml or set QUALYS_USERNAME")
    
    if not qualys_config.password or qualys_config.password == 'your_qualys_password':
        logger.warning("Qualys password not configured. Please update config.yaml or set QUALYS_PASSWORD")
    
    # Extract API config
    api_section = yaml_config.get('api', {})
    api_config = APIConfig(
        endpoint=api_section.get('endpoint', '/cloudview-api/rest/v1/aws/connectors'),
        default_page_size=api_section.get('default_page_size', 50),
        timeout_seconds=api_section.get('timeout_seconds', 30),
    )
    
    return Config(qualys=qualys_config, api=api_config)


def get_config() -> Config:
    """
    Get configuration singleton.
    
    Returns:
        Config object
    """
    return load_config()


if __name__ == "__main__":
    # Test configuration loading
    try:
        config = load_config()
        print("Configuration loaded successfully!")
        print(f"  Base URL: {config.qualys.base_url}")
        print(f"  Username: {config.qualys.username}")
        print(f"  Password: {'*' * len(config.qualys.password)}")
        print(f"  Endpoint: {config.api.endpoint}")
        print(f"  Page Size: {config.api.default_page_size}")
        print(f"  Timeout: {config.api.timeout_seconds}s")
    except FileNotFoundError as e:
        print(f"Error: {e}")
