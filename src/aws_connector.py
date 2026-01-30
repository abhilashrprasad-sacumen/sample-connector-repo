# src/aws_connector.py

"""
AWS CloudView Connector with Baseline Schema
==============================================

This connector fetches AWS connector data from Qualys CloudView API
and transforms it to match the BASELINE schema.

The baseline schema is intentionally different from the actual API response
to demonstrate how CARE (Connector Auto Repair Engine) can detect drift.

Endpoint: https://qualysguard.qg2.apps.qualys.eu/cloudview-api/rest/v1/aws/connectors
"""

import requests
import logging
from typing import Dict, List, Optional, Any

from baseline_schema import (
    ConnectorBaselineSchema,
    PaginationBaselineSchema,
    SortSchema,
    AWSConnectorsResponseBaselineSchema,
    BASELINE_TO_ACTUAL_FIELD_MAPPING,
    MISSING_FIELDS_IN_BASELINE,
)
from config_loader import load_config, Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSCloudViewConnector:
    """
    Connector for Qualys CloudView AWS Connectors API.
    
    This connector transforms API responses from the actual format
    to the baseline schema format.
    
    CARE can compare the baseline schema against actual API responses
    to detect schema drift (renamed fields, new fields, removed fields).
    """
    
    API_ENDPOINT = "/cloudview-api/rest/v1/aws/connectors"
    
    def __init__(
        self, 
        base_url: Optional[str] = None, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        config: Optional[Config] = None
    ):
        """
        Initialize the AWS CloudView connector.
        
        Credentials can be provided directly or loaded from config file.
        Direct parameters take precedence over config file values.
        
        Args:
            base_url: Qualys API base URL (optional if using config)
            username: Qualys API username (optional if using config)
            password: Qualys API password (optional if using config)
            config: Optional Config object. If not provided, loads from config.yaml
        """
        # Load config if not provided
        if config is None:
            try:
                config = load_config()
            except FileNotFoundError:
                config = None
        
        # Use direct parameters if provided, otherwise fall back to config
        self.base_url = (base_url or (config.qualys.base_url if config else "")).rstrip('/')
        resolved_username = username or (config.qualys.username if config else "")
        resolved_password = password or (config.qualys.password if config else "")
        
        if not self.base_url:
            raise ValueError("base_url is required. Provide it directly or in config.yaml")
        if not resolved_username:
            raise ValueError("username is required. Provide it directly or in config.yaml")
        if not resolved_password:
            raise ValueError("password is required. Provide it directly or in config.yaml")
        
        self.auth = (resolved_username, resolved_password)
        self.config = config
        
        # Configure session
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({'Content-Type': 'application/json'})
        
        # Set timeout from config if available
        self.timeout = config.api.timeout_seconds if config else 30
        self.default_page_size = config.api.default_page_size if config else 50
        
        logger.info(f"Initialized AWSCloudViewConnector for {self.base_url}")
    
    @classmethod
    def from_config(cls, config_path: Optional[str] = None) -> "AWSCloudViewConnector":
        """
        Create connector instance from config file.
        
        Args:
            config_path: Optional path to config file. Uses default if not provided.
            
        Returns:
            Configured AWSCloudViewConnector instance
        """
        from pathlib import Path
        config = load_config(Path(config_path) if config_path else None)
        return cls(config=config)
    
    def get_connectors(
        self,
        page: int = 0,
        per_page: int = 50
    ) -> AWSConnectorsResponseBaselineSchema:
        """
        Fetch AWS connectors and transform to baseline schema.
        
        Args:
            page: Page number (0-indexed)
            per_page: Number of items per page
            
        Returns:
            AWSConnectorsResponseBaselineSchema: Response in baseline format
            
        Note:
            The actual API uses different field names (pageNumber, pageSize).
            This connector transforms the response to baseline format.
        """
        endpoint = f"{self.base_url}{self.API_ENDPOINT}"
        
        # Actual API uses pageNumber and pageSize, but we expose page and per_page
        params = {
            'pageNumber': page,  # Actual API field name
            'pageSize': per_page,  # Actual API field name
        }
        
        logger.info(f"Fetching AWS connectors from {endpoint}")
        
        try:
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            actual_response = response.json()
            
            # Transform actual response to baseline schema
            baseline_response = self._transform_to_baseline(actual_response)
            
            logger.info(f"Retrieved {len(baseline_response.content)} connectors")
            return baseline_response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def _transform_to_baseline(
        self, 
        actual_response: Dict[str, Any]
    ) -> AWSConnectorsResponseBaselineSchema:
        """
        Transform actual API response to baseline schema format.
        
        This is where the field name transformations happen.
        CARE can detect when actual API changes break this transformation.
        
        Args:
            actual_response: Raw response from Qualys API
            
        Returns:
            Response transformed to baseline schema format
        """
        # Transform each connector in content array
        baseline_connectors = []
        for connector in actual_response.get('content', []):
            baseline_connector = self._transform_connector(connector)
            baseline_connectors.append(baseline_connector)
        
        # Transform pagination (pageable object)
        actual_pageable = actual_response.get('pageable', {})
        actual_sort = actual_pageable.get('sort', {})
        
        baseline_pageable = PaginationBaselineSchema(
            page=actual_pageable.get('pageNumber', 0),  # Renamed: pageNumber -> page
            per_page=actual_pageable.get('pageSize', 50),  # Renamed: pageSize -> per_page
            sort=SortSchema(
                sorted=actual_sort.get('sorted', False),
                empty=actual_sort.get('empty', True),
                unsorted=actual_sort.get('unsorted', True),
            ),
            offset=actual_pageable.get('offset', 0),
            paged=actual_pageable.get('paged', True),
            unpaged=actual_pageable.get('unpaged', False),
        )
        
        # Transform root level sort
        actual_root_sort = actual_response.get('sort', {})
        baseline_root_sort = SortSchema(
            sorted=actual_root_sort.get('sorted', False),
            empty=actual_root_sort.get('empty', True),
            unsorted=actual_root_sort.get('unsorted', True),
        )
        
        # Build baseline response with renamed fields
        baseline_response = AWSConnectorsResponseBaselineSchema(
            content=baseline_connectors,
            pageable=baseline_pageable,
            total_pages=actual_response.get('totalPages', 0),  # Renamed: totalPages -> total_pages
            total_count=actual_response.get('totalElements', 0),  # Renamed: totalElements -> total_count
            count=actual_response.get('numberOfElements', 0),  # Renamed: numberOfElements -> count
            last=actual_response.get('last', True),
            number=actual_response.get('number', 0),
            size=actual_response.get('size', 50),
            sort=baseline_root_sort,
            first=actual_response.get('first', True),
            empty=actual_response.get('empty', False),
        )
        
        return baseline_response
    
    def _transform_connector(self, connector: Dict[str, Any]) -> ConnectorBaselineSchema:
        """
        Transform a single connector from actual to baseline schema.
        
        Field Transformations:
        - connectorId -> connector_id
        - totalAssets -> asset_count
        - lastSyncedOn -> last_sync_time
        - nextSyncedOn -> next_sync_time
        - awsAccountId -> aws_account
        - isGovCloud -> gov_cloud
        - isChinaRegion -> china_region
        - isDisabled -> disabled
        - remediationEnabled -> remediation_active
        - pollingFrequency.hours -> polling_interval_hours (flattened)
        - isPortalConnector -> portal_connector
        - qualysTags -> tags
        
        Missing Fields (not included in baseline):
        - portalConnectorUuid
        - baseAccountId
        - externalId
        - error
        """
        # Extract polling frequency hours (flattening nested object)
        polling_freq = connector.get('pollingFrequency', {})
        polling_hours = polling_freq.get('hours', 24) if isinstance(polling_freq, dict) else 24
        
        baseline_connector = ConnectorBaselineSchema(
            # Core identification
            name=connector.get('name', ''),
            connector_id=connector.get('connectorId', ''),  # Renamed
            description=connector.get('description', ''),
            provider=connector.get('provider', 'AWS'),
            
            # Status - Renamed fields
            state=connector.get('state', ''),
            asset_count=connector.get('totalAssets', 0),  # Renamed
            last_sync_time=connector.get('lastSyncedOn', ''),  # Renamed
            next_sync_time=connector.get('nextSyncedOn', ''),  # Renamed
            
            # AWS specific - Renamed fields
            aws_account=connector.get('awsAccountId', ''),  # Renamed
            arn=connector.get('arn', ''),
            gov_cloud=connector.get('isGovCloud', False),  # Renamed
            china_region=connector.get('isChinaRegion', False),  # Renamed
            
            # Configuration - Renamed/Flattened fields
            disabled=connector.get('isDisabled', False),  # Renamed
            remediation_active=connector.get('remediationEnabled', False),  # Renamed
            polling_interval_hours=polling_hours,  # Flattened from pollingFrequency.hours
            
            # Portal - Renamed (some fields intentionally missing)
            portal_connector=connector.get('isPortalConnector', False),  # Renamed
            # NOTE: portalConnectorUuid is NOT included in baseline
            # NOTE: baseAccountId is NOT included in baseline
            # NOTE: externalId is NOT included in baseline
            # NOTE: error is NOT included in baseline
            
            # Tags - Renamed
            tags=connector.get('qualysTags', []),  # Renamed
        )
        
        return baseline_connector
    
    def get_connector_by_id(self, connector_id: str) -> Optional[ConnectorBaselineSchema]:
        """
        Get a specific connector by ID.
        
        Args:
            connector_id: The connector ID to search for
            
        Returns:
            ConnectorBaselineSchema if found, None otherwise
        """
        response = self.get_connectors()
        
        for connector in response.content:
            if connector.connector_id == connector_id:
                return connector
        
        return None
    
    def get_connectors_by_account(self, aws_account: str) -> List[ConnectorBaselineSchema]:
        """
        Get all connectors for a specific AWS account.
        
        Args:
            aws_account: AWS account ID
            
        Returns:
            List of connectors for the account
        """
        response = self.get_connectors()
        
        return [c for c in response.content if c.aws_account == aws_account]
    
    def get_active_connectors(self) -> List[ConnectorBaselineSchema]:
        """
        Get all active (non-disabled) connectors.
        
        Returns:
            List of active connectors
        """
        response = self.get_connectors()
        
        return [c for c in response.content if not c.disabled]
    
    def get_raw_response(self, page: int = 0, per_page: int = 50) -> Dict[str, Any]:
        """
        Get the raw API response without transformation.
        
        This is useful for CARE to compare actual vs baseline schemas.
        
        Args:
            page: Page number
            per_page: Items per page
            
        Returns:
            Raw API response as dictionary
        """
        endpoint = f"{self.base_url}{self.API_ENDPOINT}"
        
        params = {
            'pageNumber': page,
            'pageSize': per_page,
        }
        
        response = self.session.get(endpoint, params=params, timeout=30)
        response.raise_for_status()
        
        return response.json()


# ============================================
# EXAMPLE USAGE AND TESTING
# ============================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS CloudView Connector Demo")
    parser.add_argument(
        "--live", 
        action="store_true", 
        help="Use live API instead of mock data"
    )
    parser.add_argument(
        "--config", 
        type=str, 
        default=None,
        help="Path to config file (default: config.yaml in project root)"
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("AWS CloudView Connector - Baseline Schema Demo")
    print("=" * 60)
    
    if args.live:
        # =====================================
        # LIVE MODE - Use actual API endpoint
        # =====================================
        print("\n[MODE: LIVE API]")
        print("-" * 60)
        
        try:
            # Load connector from config
            if args.config:
                connector = AWSCloudViewConnector.from_config(args.config)
            else:
                connector = AWSCloudViewConnector.from_config()
            
            print(f"Connecting to: {connector.base_url}")
            print(f"Endpoint: {connector.API_ENDPOINT}")
            
            # Fetch actual data
            print("\nFetching connectors from live API...")
            baseline_response = connector.get_connectors()
            
            print(f"\n[SUCCESS] Retrieved {len(baseline_response.content)} connector(s)")
            
            # Display results
            print("\n[CONNECTORS FOUND]")
            for i, conn in enumerate(baseline_response.content):
                print(f"\n  Connector {i + 1}:")
                print(f"    Name: {conn.name}")
                print(f"    ID: {conn.connector_id}")
                print(f"    AWS Account: {conn.aws_account}")
                print(f"    State: {conn.state}")
                print(f"    Assets: {conn.asset_count}")
                print(f"    Last Sync: {conn.last_sync_time}")
            
            print("\n[PAGINATION INFO]")
            print(f"  Page: {baseline_response.pageable.page + 1} of {baseline_response.total_pages}")
            print(f"  Total Connectors: {baseline_response.total_count}")
            
        except FileNotFoundError as e:
            print(f"\n[ERROR] {e}")
            print("\nTo use live mode:")
            print("  1. Copy config.example.yaml to config.yaml")
            print("  2. Fill in your Qualys credentials")
            print("  3. Run again with --live flag")
        except Exception as e:
            print(f"\n[ERROR] API call failed: {e}")
    
    else:
        # =====================================
        # MOCK MODE - Use sample data
        # =====================================
        print("\n[MODE: MOCK DATA]")
        print("-" * 60)
        print("Using sample response data for demonstration.")
        print("Run with --live flag to use actual API.")
        
        # Sample actual response (as provided)
        sample_actual_response = {
            "content": [
                {
                    "name": "AWS-102716399460",
                    "connectorId": "22eb46aa-7bc4-380c-90f7-a6f15972ed39",
                    "description": "",
                    "provider": "AWS",
                    "state": "Completed successfully",
                    "totalAssets": 496,
                    "lastSyncedOn": "Fri Jan 30 06:29:04 GMT 2026",
                    "nextSyncedOn": "Fri Jan 30 06:28:05 GMT 2026",
                    "remediationEnabled": False,
                    "qualysTags": [],
                    "isGovCloud": False,
                    "isChinaRegion": False,
                    "awsAccountId": "102716399460",
                    "isDisabled": False,
                    "pollingFrequency": {
                        "hours": 24,
                        "minutes": 0
                    },
                    "error": "",
                    "baseAccountId": "805950163170",
                    "externalId": "EU2-2792719",
                    "arn": "arn:aws:iam::102716399460:role/QualysCSMPReadOnly",
                    "portalConnectorUuid": "abe5da7b-d91f-475b-8084-45c5c731d80b",
                    "isPortalConnector": True
                }
            ],
            "pageable": {
                "pageNumber": 0,
                "pageSize": 50,
                "sort": {
                    "sorted": True,
                    "empty": False,
                    "unsorted": False
                },
                "offset": 0,
                "paged": True,
                "unpaged": False
            },
            "totalPages": 1,
            "totalElements": 1,
            "last": True,
            "number": 0,
            "size": 50,
            "numberOfElements": 1,
            "sort": {
                "sorted": True,
                "empty": False,
                "unsorted": False
            },
            "first": True,
            "empty": False
        }
        
        # Create a mock connector instance for demonstration
        class MockAWSCloudViewConnector(AWSCloudViewConnector):
            def __init__(self):
                self.base_url = "https://qualysguard.qg2.apps.qualys.eu"
                self.timeout = 30
                self.default_page_size = 50
                logger.info("Mock connector initialized")
            
            def get_connectors(self, page: int = 0, per_page: int = 50):
                return self._transform_to_baseline(sample_actual_response)
        
        # Demo transformation
        connector = MockAWSCloudViewConnector()
        baseline_response = connector.get_connectors()
        
        print("\n[BASELINE SCHEMA TRANSFORMATION DEMO]")
        print("-" * 60)
        
        print("\n[FIELD RENAMING EXAMPLES]")
        print(f"  connectorId -> connector_id: {baseline_response.content[0].connector_id}")
        print(f"  totalAssets -> asset_count: {baseline_response.content[0].asset_count}")
        print(f"  awsAccountId -> aws_account: {baseline_response.content[0].aws_account}")
        print(f"  isGovCloud -> gov_cloud: {baseline_response.content[0].gov_cloud}")
        print(f"  pollingFrequency.hours -> polling_interval_hours: {baseline_response.content[0].polling_interval_hours}")
        
        print("\n[PAGINATION FIELD RENAMING]")
        print(f"  pageNumber -> page: {baseline_response.pageable.page}")
        print(f"  pageSize -> per_page: {baseline_response.pageable.per_page}")
        print(f"  totalElements -> total_count: {baseline_response.total_count}")
        
        print("\n[MISSING FIELDS - intentionally excluded from baseline]")
        for field in MISSING_FIELDS_IN_BASELINE:
            print(f"  - {field}")
        
        print("\n[FULL BASELINE RESPONSE]")
        print(baseline_response.model_dump_json(indent=2))

