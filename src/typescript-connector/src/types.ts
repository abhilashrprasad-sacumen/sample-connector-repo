/**
 * Type definitions for Qualys AWS Connectors API.
 * 
 * IMPORTANT: These types use an OUTDATED baseline schema with intentional differences
 * from the actual API response. This is designed for CARE (Connector Auto-Repair Engine)
 * testing to demonstrate automatic schema change detection and code patching.
 * 
 * Intentional Differences:
 * 1. Field names use snake_case instead of actual camelCase
 * 2. 'status' field is used instead of actual 'state' field
 * 3. Missing fields: nextSyncedOn, remediationEnabled, qualysTags, portalConnectorUuid, isPortalConnector
 */

/**
 * Polling frequency configuration for a connector.
 */
export interface PollingFrequency {
    hours: number;
    minutes: number;
}

/**
 * AWS Connector data model.
 * 
 * NOTE: This model is based on the BASELINE SCHEMA which has intentional
 * differences from the actual API response for CARE testing purposes.
 */
export interface AWSConnector {
    name: string;
    connector_id: string;        // Actual API field: connectorId
    description: string;
    provider: string;
    status: string;              // Actual API field: state (RENAMED FIELD)
    total_assets: number;        // Actual API field: totalAssets
    last_synced_on: string;      // Actual API field: lastSyncedOn
    is_gov_cloud: boolean;       // Actual API field: isGovCloud
    is_china_region: boolean;    // Actual API field: isChinaRegion
    aws_account_id: string;      // Actual API field: awsAccountId
    is_disabled: boolean;        // Actual API field: isDisabled
    polling_frequency: PollingFrequency;
    error: string;
    base_account_id: string;     // Actual API field: baseAccountId
    external_id: string;         // Actual API field: externalId
    arn: string;
    // MISSING FIELDS from actual API:
    // - nextSyncedOn
    // - remediationEnabled
    // - qualysTags
    // - portalConnectorUuid
    // - isPortalConnector
}

/**
 * Pagination information from API response.
 */
export interface PaginationInfo {
    page_number: number;         // Actual API field: pageNumber
    page_size: number;           // Actual API field: pageSize
    total_pages: number;         // Actual API field: totalPages
    total_elements: number;      // Actual API field: totalElements
    number_of_elements: number;  // Actual API field: numberOfElements
}

/**
 * Complete response from the AWS Connectors API.
 */
export interface ConnectorResponse {
    connectors: AWSConnector[];
    pagination: PaginationInfo;
    is_first: boolean;
    is_last: boolean;
    is_empty: boolean;
}

/**
 * Raw API response structure (actual camelCase fields from API).
 * This is what we actually receive from the API.
 */
export interface RawAPIResponse {
    content: any[];
    pageable: {
        pageNumber?: number;
        page_number?: number;
        pageSize?: number;
        page_size?: number;
        sort?: any;
        offset?: number;
        paged?: boolean;
        unpaged?: boolean;
    };
    totalPages?: number;
    total_pages?: number;
    totalElements?: number;
    total_elements?: number;
    numberOfElements?: number;
    number_of_elements?: number;
    last?: boolean;
    number?: number;
    size?: number;
    sort?: any;
    first?: boolean;
    empty?: boolean;
}
