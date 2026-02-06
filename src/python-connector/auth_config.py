"""
Authentication configuration for Qualys API connector.
Uses Basic Authentication with username and password.
"""

import os
from dataclasses import dataclass
from typing import Optional

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use environment variables directly


@dataclass
class QualysAuthConfig:
    """Configuration for Qualys API authentication."""
    
    # Base URL for the Qualys API
    base_url: str = "https://qualysguard.qg2.apps.qualys.eu"
    
    # API credentials - should be set via environment variables in production
    username: str = ""
    password: str = ""
    
    # Request timeout in seconds
    timeout: int = 30
    
    # SSL verification
    verify_ssl: bool = True
    
    @classmethod
    def from_env(cls) -> "QualysAuthConfig":
        """
        Create configuration from environment variables.
        
        Expected environment variables:
        - QUALYS_BASE_URL: Base URL for Qualys API (optional, has default)
        - QUALYS_USERNAME: API username (required)
        - QUALYS_PASSWORD: API password (required)
        - QUALYS_TIMEOUT: Request timeout in seconds (optional)
        - QUALYS_VERIFY_SSL: Whether to verify SSL certificates (optional)
        """
        return cls(
            base_url=os.getenv("QUALYS_BASE_URL", "https://qualysguard.qg2.apps.qualys.eu"),
            username=os.getenv("QUALYS_USERNAME", ""),
            password=os.getenv("QUALYS_PASSWORD", ""),
            timeout=int(os.getenv("QUALYS_TIMEOUT", "30")),
            verify_ssl=os.getenv("QUALYS_VERIFY_SSL", "true").lower() == "true"
        )
    
    def validate(self) -> bool:
        """Validate that required credentials are provided."""
        if not self.username or not self.password:
            raise ValueError("QUALYS_USERNAME and QUALYS_PASSWORD environment variables must be set")
        return True
    
    def get_auth_tuple(self) -> tuple:
        """Return authentication tuple for requests library."""
        return (self.username, self.password)


# Default configuration instance
default_config = QualysAuthConfig.from_env()
