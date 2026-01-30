# src/baseline_schema.py

"""
Baseline Schema for Qualys CloudView AWS Connectors API
=========================================================

Endpoint: https://qualysguard.qg2.apps.qualys.eu/cloudview-api/rest/v1/aws/connectors

This baseline schema is INTENTIONALLY DIFFERENT from the actual API response.
The CARE (Connector Auto Repair Engine) uses this to detect schema drift.

DIFFERENCES FROM ACTUAL API RESPONSE:
=====================================

RENAMED FIELDS:
- connectorId -> connector_id
- totalAssets -> asset_count
- lastSyncedOn -> last_sync_time
- nextSyncedOn -> next_sync_time
- awsAccountId -> aws_account
- isGovCloud -> gov_cloud
- isChinaRegion -> china_region
- isDisabled -> disabled
- remediationEnabled -> remediation_active
- pollingFrequency -> polling_interval_hours (flattened)
- isPortalConnector -> portal_connector
- qualysTags -> tags

MISSING FIELDS (intentionally omitted):
- portalConnectorUuid
- baseAccountId
- externalId
- error

PAGINATION FIELD RENAMES:
- pageNumber -> page
- pageSize -> per_page
- totalPages -> total_pages
- totalElements -> total_count
- numberOfElements -> count
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ============================================
# CONNECTOR CONTENT SCHEMA (Single Connector)
# ============================================

class ConnectorBaselineSchema(BaseModel):
    """
    Baseline schema for a single AWS connector.
    
    This schema intentionally differs from the actual API response
    to allow CARE to detect and repair schema drift.
    """
    
    # Core identification - RENAMED from original
    name: str = Field(..., description="Connector name")
    connector_id: str = Field(..., description="Unique connector identifier (renamed from 'connectorId')")
    description: str = Field(default="", description="Connector description")
    provider: str = Field(default="AWS", description="Cloud provider")
    
    # Status - RENAMED from original
    state: str = Field(..., description="Current connector state")
    asset_count: int = Field(..., description="Total assets count (renamed from 'totalAssets')")
    last_sync_time: str = Field(..., description="Last sync timestamp (renamed from 'lastSyncedOn')")
    next_sync_time: str = Field(default="", description="Next sync timestamp (renamed from 'nextSyncedOn')")
    
    # AWS specific - RENAMED from original
    aws_account: str = Field(..., description="AWS Account ID (renamed from 'awsAccountId')")
    arn: str = Field(..., description="AWS IAM Role ARN")
    gov_cloud: bool = Field(default=False, description="Is GovCloud (renamed from 'isGovCloud')")
    china_region: bool = Field(default=False, description="Is China region (renamed from 'isChinaRegion')")
    
    # Configuration - RENAMED/FLATTENED from original
    disabled: bool = Field(default=False, description="Is disabled (renamed from 'isDisabled')")
    remediation_active: bool = Field(default=False, description="Remediation enabled (renamed from 'remediationEnabled')")
    polling_interval_hours: int = Field(default=24, description="Polling frequency in hours (flattened from 'pollingFrequency.hours')")
    
    # Portal - RENAMED and MISSING fields
    portal_connector: bool = Field(default=False, description="Is portal connector (renamed from 'isPortalConnector')")
    # NOTE: portalConnectorUuid is INTENTIONALLY MISSING from baseline
    # NOTE: baseAccountId is INTENTIONALLY MISSING from baseline
    # NOTE: externalId is INTENTIONALLY MISSING from baseline
    # NOTE: error is INTENTIONALLY MISSING from baseline
    
    # Tags - RENAMED from original
    tags: List[str] = Field(default=[], description="Qualys tags (renamed from 'qualysTags')")

    class Config:
        """Pydantic config."""
        extra = "forbid"  # Fail if extra fields are present


# ============================================
# PAGINATION SCHEMA
# ============================================

class SortSchema(BaseModel):
    """Sort information schema."""
    sorted: bool = Field(default=False)
    empty: bool = Field(default=True)
    unsorted: bool = Field(default=True)


class PaginationBaselineSchema(BaseModel):
    """
    Baseline schema for pagination.
    
    RENAMED from original:
    - pageNumber -> page
    - pageSize -> per_page
    """
    page: int = Field(default=0, description="Current page number (renamed from 'pageNumber')")
    per_page: int = Field(default=50, description="Page size (renamed from 'pageSize')")
    sort: SortSchema = Field(default_factory=SortSchema)
    offset: int = Field(default=0)
    paged: bool = Field(default=True)
    unpaged: bool = Field(default=False)


# ============================================
# FULL RESPONSE SCHEMA
# ============================================

class AWSConnectorsResponseBaselineSchema(BaseModel):
    """
    Baseline schema for the full AWS connectors API response.
    
    DIFFERENCES FROM ACTUAL RESPONSE:
    - content uses ConnectorBaselineSchema with renamed fields
    - pageable uses PaginationBaselineSchema with renamed fields
    - totalPages -> total_pages
    - totalElements -> total_count
    - numberOfElements -> count
    """
    
    # Content array with baseline connector schema
    content: List[ConnectorBaselineSchema] = Field(
        default=[],
        description="List of AWS connectors"
    )
    
    # Pagination - uses renamed schema
    pageable: PaginationBaselineSchema = Field(default_factory=PaginationBaselineSchema)
    
    # Page metadata - RENAMED from original
    total_pages: int = Field(default=0, description="Total pages (renamed from 'totalPages')")
    total_count: int = Field(default=0, description="Total elements (renamed from 'totalElements')")
    count: int = Field(default=0, description="Number of elements (renamed from 'numberOfElements')")
    
    # Unchanged fields
    last: bool = Field(default=True)
    number: int = Field(default=0)
    size: int = Field(default=50)
    sort: SortSchema = Field(default_factory=SortSchema)
    first: bool = Field(default=True)
    empty: bool = Field(default=False)

    class Config:
        """Pydantic config."""
        extra = "forbid"


# ============================================
# FIELD MAPPING FOR CARE ENGINE
# ============================================

# This mapping helps CARE identify how fields should be transformed
BASELINE_TO_ACTUAL_FIELD_MAPPING = {
    # Connector fields
    "connector_id": "connectorId",
    "asset_count": "totalAssets",
    "last_sync_time": "lastSyncedOn",
    "next_sync_time": "nextSyncedOn",
    "aws_account": "awsAccountId",
    "gov_cloud": "isGovCloud",
    "china_region": "isChinaRegion",
    "disabled": "isDisabled",
    "remediation_active": "remediationEnabled",
    "polling_interval_hours": "pollingFrequency.hours",
    "portal_connector": "isPortalConnector",
    "tags": "qualysTags",
    
    # Pagination fields
    "page": "pageNumber",
    "per_page": "pageSize",
    "total_pages": "totalPages",
    "total_count": "totalElements",
    "count": "numberOfElements",
}

# Fields that exist in actual API but are MISSING from baseline
MISSING_FIELDS_IN_BASELINE = [
    "portalConnectorUuid",
    "baseAccountId", 
    "externalId",
    "error",
]

# Fields that are FLATTENED in baseline
FLATTENED_FIELDS = {
    "polling_interval_hours": {
        "source_path": "pollingFrequency.hours",
        "description": "Flattened from nested pollingFrequency object"
    }
}
