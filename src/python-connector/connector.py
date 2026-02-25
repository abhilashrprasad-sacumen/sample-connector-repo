"""
Qualys AWS Connectors API Connector

This connector fetches AWS connector information from the Qualys CloudView API.

IMPORTANT: This connector uses an OUTDATED baseline schema with intentional differences
from the actual API response. This is designed for CARE (Connector Auto-Repair Engine)
testing to demonstrate automatic schema change detection and code patching.

Intentional Differences:
1. Field names use snake_case instead of actual camelCase
2. 'status' field is used instead of actual 'state' field
3. Missing fields: nextSyncedOn, remediationEnabled, qualysTags, portalConnectorUuid, isPortalConnector
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

import requests

from auth_config import QualysAuthConfig, default_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PollingFrequency:
    """Polling frequency configuration for a connector."""
    hours: int = 0
    minutes: int = 0


@dataclass
class AWSConnector:
    """
    Data class representing an AWS Connector from Qualys.
    
    NOTE: This model is based on the BASELINE SCHEMA which has intentional
    differences from the actual API response for CARE testing purposes.
    """
    name: str
    connector_id: str  # Actual API field: connectorId
    description: str
    provider: str
    status: str  # Actual API field: state (RENAMED FIELD)
    total_assets: int  # Actual API field: totalAssets
    last_synced_on: str  # Actual API field: lastSyncedOn
    is_gov_cloud: bool  # Actual API field: isGovCloud
    is_china_region: bool  # Actual API field: isChinaRegion
    aws_account_id: str  # Actual API field: awsAccountId
    is_disabled: bool  # Actual API field: isDisabled
    polling_frequency: PollingFrequency
    error: str
    base_account_id: str  # Actual API field: baseAccountId
    external_id: str  # Actual API field: externalId
    arn: str
    # MISSING FIELDS from actual API:
    # - nextSyncedOn
    # - remediationEnabled
    # - qualysTags
    # - portalConnectorUuid
    # - isPortalConnector


@dataclass
class PaginationInfo:
    """Pagination information from API response."""
    page_number: int  # Actual API field: pageNumber
    page_size: int  # Actual API field: pageSize
    total_pages: int  # Actual API field: totalPages
    total_elements: int  # Actual API field: totalElements
    number_of_elements: int  # Actual API field: numberOfElements


@dataclass
class ConnectorResponse:
    """Complete response from the AWS Connectors API."""
    connectors: List[AWSConnector]
    pagination: PaginationInfo
    is_first: bool
    is_last: bool
    is_empty: bool


class QualysAWSConnector:
    """
    Connector for Qualys CloudView AWS Connectors API.
    
    This connector fetches AWS connector information using Basic Authentication.
    It maps API response fields based on the BASELINE SCHEMA which intentionally
    differs from the actual API response for CARE testing purposes.
    """
    
    ENDPOINT = "/cloudview-api/rest/v1/aws/connectors"
    
    def __init__(self, config: Optional[QualysAuthConfig] = None):
        """
        Initialize the connector with authentication configuration.
        
        Args:
            config: QualysAuthConfig instance. If None, uses default config from env vars.
        """
        self.config = config or default_config
        self.config.validate()
        self.session = requests.Session()
        self.session.auth = self.config.get_auth_tuple()
        self.session.verify = self.config.verify_ssl
        
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from base URL and endpoint."""
        return f"{self.config.base_url.rstrip('/')}{endpoint}"
    
    def _parse_polling_frequency(self, data: Dict[str, Any]) -> PollingFrequency:
        """
        Parse polling frequency from API response.
        
        Uses baseline schema field names (snake_case) but actual API returns camelCase.
        """
        # NOTE: Baseline schema expects 'polling_frequency' but API returns 'pollingFrequency'
        freq_data = data.get("polling_frequency", data.get("pollingFrequency", {}))
        return PollingFrequency(
            hours=freq_data.get("hours", 0),
            minutes=freq_data.get("minutes", 0)
        )
    
    def _parse_connector(self, data: Dict[str, Any]) -> AWSConnector:
        """
        Parse a single connector from API response.
        
        IMPORTANT: This method uses BASELINE SCHEMA field mappings which differ
        from the actual API response. CARE should detect and fix these mismatches.
        """
        return AWSConnector(
            name=data.get("name", ""),
            # Using 'connector_id' but API returns 'connectorId'
            connector_id=data.get("connector_id", data.get("connectorId", "")),
            description=data.get("description", ""),
            provider=data.get("provider", ""),
            # Using 'status' but API returns 'state' (FIELD RENAMED)
            status=data.get("status", data.get("state", "")),
            # Using 'total_assets' but API returns 'totalAssets'
            total_assets=data.get("total_assets", data.get("totalAssets", 0)),
            # Using 'last_synced_on' but API returns 'lastSyncedOn'
            last_synced_on=data.get("last_synced_on", data.get("lastSyncedOn", "")),
            # Using 'is_gov_cloud' but API returns 'isGovCloud'
            is_gov_cloud=data.get("is_gov_cloud", data.get("isGovCloud", False)),
            # Using 'is_china_region' but API returns 'isChinaRegion'
            is_china_region=data.get("is_china_region", data.get("isChinaRegion", False)),
            # Using 'aws_account_id' but API returns 'awsAccountId'
            aws_account_id=data.get("aws_account_id", data.get("awsAccountId", "")),
            # Using 'is_disabled' but API returns 'isDisabled'
            is_disabled=data.get("is_disabled", data.get("isDisabled", False)),
            polling_frequency=self._parse_polling_frequency(data),
            error=data.get("error", ""),
            # Using 'base_account_id' but API returns 'baseAccountId'
            base_account_id=data.get("base_account_id", data.get("baseAccountId", "")),
            # Using 'external_id' but API returns 'externalId'
            external_id=data.get("external_id", data.get("externalId", "")),
            arn=data.get("arn", "")
            # MISSING FIELDS that exist in actual API but not captured:
            # - nextSyncedOn
            # - remediationEnabled
            # - qualysTags
            # - portalConnectorUuid
            # - isPortalConnector
        )
    
    def _parse_pagination(self, data: Dict[str, Any]) -> PaginationInfo:
        """
        Parse pagination information from API response.
        
        Uses baseline schema field names which differ from actual API response.
        """
        pageable = data.get("pageable", {})
        return PaginationInfo(
            # Using 'page_number' but API returns 'pageNumber'
            page_number=pageable.get("page_number", pageable.get("pageNumber", 0)),
            # Using 'page_size' but API returns 'pageSize'
            page_size=pageable.get("page_size", pageable.get("pageSize", 0)),
            # Using 'total_pages' but API returns 'totalPages'
            total_pages=data.get("total_pages", data.get("totalPages", 0)),
            # Using 'total_elements' but API returns 'totalElements'
            total_elements=data.get("total_elements", data.get("totalElements", 0)),
            # Using 'number_of_elements' but API returns 'numberOfElements'
            number_of_elements=data.get("number_of_elements", data.get("numberOfElements", 0))
        )
    
    def fetch_connectors(self, page: int = 0, page_size: int = 50) -> ConnectorResponse:
        """
        Fetch AWS connectors from Qualys CloudView API.
        
        Args:
            page: Page number (0-indexed)
            page_size: Number of items per page
            
        Returns:
            ConnectorResponse containing list of connectors and pagination info
            
        Raises:
            requests.RequestException: If API call fails
            ValueError: If response cannot be parsed
        """
        url = self._build_url(self.ENDPOINT)
        params = {
            "pageNo": page,
            "pageSize": page_size
        }
        
        logger.info(f"Fetching AWS connectors from {url}")
        
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched {len(data.get('content', []))} connectors")
            
            return self._parse_response(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch connectors: {e}")
            raise
        except (KeyError, ValueError) as e:
            logger.error(f"Failed to parse response: {e}")
            raise ValueError(f"Invalid API response format: {e}")
    
    def _parse_response(self, data: Dict[str, Any]) -> ConnectorResponse:
        """Parse full API response into ConnectorResponse object."""
        content = data.get("content", [])
        connectors = [self._parse_connector(c) for c in content]
        pagination = self._parse_pagination(data)
        
        return ConnectorResponse(
            connectors=connectors,
            pagination=pagination,
            is_first=data.get("first", True),
            is_last=data.get("last", True),
            is_empty=data.get("empty", False)
        )
    
    def get_all_connectors(self) -> List[AWSConnector]:
        """
        Fetch all AWS connectors, handling pagination automatically.
        
        Returns:
            List of all AWSConnector objects
        """
        all_connectors = []
        page = 0
        
        while True:
            response = self.fetch_connectors(page=page)
            all_connectors.extend(response.connectors)
            
            if response.is_last:
                break
            page += 1
        
        logger.info(f"Fetched total of {len(all_connectors)} connectors")
        return all_connectors
    
    def get_connector_by_id(self, connector_id: str) -> Optional[AWSConnector]:
        """
        Find a specific connector by its ID.
        
        Args:
            connector_id: The connector UUID to search for
            
        Returns:
            AWSConnector if found, None otherwise
        """
        connectors = self.get_all_connectors()
        for connector in connectors:
            if connector.connector_id == connector_id:
                return connector
        return None
    
    def to_normalized_dict(self, connector: AWSConnector) -> Dict[str, Any]:
        """
        Convert connector to normalized dictionary format.
        
        This uses the BASELINE SCHEMA field names (snake_case) which differ
        from the actual API response (camelCase). CARE should detect this mismatch.
        """
        return {
            "name": connector.name,
            "connector_id": connector.connector_id,  # Should be 'connectorId'
            "description": connector.description,
            "provider": connector.provider,
            "status": connector.status,  # Should be 'state'
            "total_assets": connector.total_assets,  # Should be 'totalAssets'
            "last_synced_on": connector.last_synced_on,  # Should be 'lastSyncedOn'
            "is_gov_cloud": connector.is_gov_cloud,  # Should be 'isGovCloud'
            "is_china_region": connector.is_china_region,  # Should be 'isChinaRegion'
            "aws_account_id": connector.aws_account_id,  # Should be 'awsAccountId'
            "is_disabled": connector.is_disabled,  # Should be 'isDisabled'
            "polling_frequency": {  # Should be 'pollingFrequency'
                "hours": connector.polling_frequency.hours,
                "minutes": connector.polling_frequency.minutes
            },
            "error": connector.error,
            "base_account_id": connector.base_account_id,  # Should be 'baseAccountId'
            "external_id": connector.external_id,  # Should be 'externalId'
            "arn": connector.arn
            # MISSING: nextSyncedOn, remediationEnabled, qualysTags, portalConnectorUuid, isPortalConnector
        }


def main():
    """Main function to demonstrate connector usage."""
    try:
        # Initialize connector (will use environment variables for auth)
        connector = QualysAWSConnector()
        
        # Fetch connectors
        response = connector.fetch_connectors()
        
        print(f"{'='*60}")
        print("QUALYS AWS CONNECTORS")
        print(f"{'='*60}")
        print(f"Total Connectors: {response.pagination.total_elements}")
        print(f"Page: {response.pagination.page_number + 1} of {response.pagination.total_pages}")
        print(f"{'='*60}\n")
        
        for conn in response.connectors:
            print(f"Name: {conn.name}")
            print(f"  Connector ID: {conn.connector_id}")
            print(f"  Provider: {conn.provider}")
            print(f"  Status: {conn.status}")  # Using 'status' but actual field is 'state'
            print(f"  Total Assets: {conn.total_assets}")
            print(f"  AWS Account ID: {conn.aws_account_id}")
            print(f"  Last Synced: {conn.last_synced_on}")
            print(f"  Is Disabled: {conn.is_disabled}")
            print(f"  ARN: {conn.arn}")
            print()
        
        # Export as normalized dict (using baseline schema field names)
        print(f"{'='*60}")
        print("NORMALIZED OUTPUT (Baseline Schema Format)")
        print(f"{'='*60}")
        for conn in response.connectors:
            normalized = connector.to_normalized_dict(conn)
            print(json.dumps(normalized, indent=2))
            
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\nError: {e}")
        print("\nPlease set the following environment variables:")
        print("  export QUALYS_USERNAME='your_username'")
        print("  export QUALYS_PASSWORD='your_password'")
    except requests.RequestException as e:
        logger.error(f"API error: {e}")


if __name__ == "__main__":
    main()
