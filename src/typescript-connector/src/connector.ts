/**
 * Qualys AWS Connectors API Connector
 * 
 * This connector fetches AWS connector information from the Qualys CloudView API.
 * 
 * IMPORTANT: This connector uses an OUTDATED baseline schema with intentional differences
 * from the actual API response. This is designed for CARE (Connector Auto-Repair Engine)
 * testing to demonstrate automatic schema change detection and code patching.
 * 
 * Intentional Differences:
 * 1. Field names use snake_case instead of actual camelCase
 * 2. 'status' field is used instead of actual 'state' field
 * 3. Missing fields: nextSyncedOn, remediationEnabled, qualysTags, portalConnectorUuid, isPortalConnector
 */

import axios, { AxiosInstance } from 'axios';
import * as https from 'https';
import {
    QualysAuthConfig,
    loadAuthConfig,
    validateAuthConfig,
    getAuthHeader,
    defaultConfig
} from './authConfig';
import {
    AWSConnector,
    PollingFrequency,
    PaginationInfo,
    ConnectorResponse,
    RawAPIResponse
} from './types';

/**
 * Connector for Qualys CloudView AWS Connectors API.
 * 
 * This connector fetches AWS connector information using Basic Authentication.
 * It maps API response fields based on the BASELINE SCHEMA which intentionally
 * differs from the actual API response for CARE testing purposes.
 */
export class QualysAWSConnector {
    private static readonly ENDPOINT = '/cloudview-api/rest/v1/aws/connectors';

    private config: QualysAuthConfig;
    private axiosInstance: AxiosInstance;

    /**
     * Initialize the connector with authentication configuration.
     * 
     * @param config - QualysAuthConfig instance. If undefined, uses default config from env vars.
     */
    constructor(config?: QualysAuthConfig) {
        this.config = config || defaultConfig;
        validateAuthConfig(this.config);

        // Create axios instance with authentication
        this.axiosInstance = axios.create({
            baseURL: this.config.baseUrl.replace(/\/$/, ''),
            timeout: this.config.timeout * 1000,
            headers: {
                'Authorization': getAuthHeader(this.config),
                'Content-Type': 'application/json'
            },
            httpsAgent: new https.Agent({
                rejectUnauthorized: this.config.verifySsl
            })
        });
    }

    /**
     * Parse polling frequency from API response.
     * 
     * Uses baseline schema field names (snake_case) but actual API returns camelCase.
     */
    private parsePollingFrequency(data: any): PollingFrequency {
        // NOTE: Baseline schema expects 'polling_frequency' but API returns 'pollingFrequency'
        const freqData = data.polling_frequency || data.pollingFrequency || {};
        return {
            hours: freqData.hours || 0,
            minutes: freqData.minutes || 0
        };
    }

    /**
     * Parse a single connector from API response.
     * 
     * IMPORTANT: This method uses BASELINE SCHEMA field mappings which differ
     * from the actual API response. CARE should detect and fix these mismatches.
     */
    private parseConnector(data: any): AWSConnector {
        return {
            name: data.name || '',
            // Using 'connector_id' but API returns 'connectorId'
            connector_id: data.connector_id || data.connectorId || '',
            description: data.description || '',
            provider: data.provider || '',
            // Using 'status' but API returns 'state' (FIELD RENAMED)
            status: data.status || data.state || '',
            // Using 'total_assets' but API returns 'totalAssets'
            total_assets: data.total_assets || data.totalAssets || 0,
            // Using 'last_synced_on' but API returns 'lastSyncedOn'
            last_synced_on: data.last_synced_on || data.lastSyncedOn || '',
            // Using 'is_gov_cloud' but API returns 'isGovCloud'
            is_gov_cloud: data.is_gov_cloud || data.isGovCloud || false,
            // Using 'is_china_region' but API returns 'isChinaRegion'
            is_china_region: data.is_china_region || data.isChinaRegion || false,
            // Using 'aws_account_id' but API returns 'awsAccountId'
            aws_account_id: data.aws_account_id || data.awsAccountId || '',
            // Using 'is_disabled' but API returns 'isDisabled'
            is_disabled: data.is_disabled || data.isDisabled || false,
            polling_frequency: this.parsePollingFrequency(data),
            error: data.error || '',
            // Using 'base_account_id' but API returns 'baseAccountId'
            base_account_id: data.base_account_id || data.baseAccountId || '',
            // Using 'external_id' but API returns 'externalId'
            external_id: data.external_id || data.externalId || '',
            arn: data.arn || ''
            // MISSING FIELDS that exist in actual API but not captured:
            // - nextSyncedOn
            // - remediationEnabled
            // - qualysTags
            // - portalConnectorUuid
            // - isPortalConnector
        };
    }

    /**
     * Parse pagination information from API response.
     * 
     * Uses baseline schema field names which differ from actual API response.
     */
    private parsePagination(data: RawAPIResponse): PaginationInfo {
        const pageable = data.pageable || {};
        return {
            // Using 'page_number' but API returns 'pageNumber'
            page_number: pageable.page_number || pageable.pageNumber || 0,
            // Using 'page_size' but API returns 'pageSize'
            page_size: pageable.page_size || pageable.pageSize || 0,
            // Using 'total_pages' but API returns 'totalPages'
            total_pages: data.total_pages || data.totalPages || 0,
            // Using 'total_elements' but API returns 'totalElements'
            total_elements: data.total_elements || data.totalElements || 0,
            // Using 'number_of_elements' but API returns 'numberOfElements'
            number_of_elements: data.number_of_elements || data.numberOfElements || 0
        };
    }

    /**
     * Parse full API response into ConnectorResponse object.
     */
    private parseResponse(data: RawAPIResponse): ConnectorResponse {
        const content = data.content || [];
        const connectors = content.map(c => this.parseConnector(c));
        const pagination = this.parsePagination(data);

        return {
            connectors,
            pagination,
            is_first: data.first !== undefined ? data.first : true,
            is_last: data.last !== undefined ? data.last : true,
            is_empty: data.empty !== undefined ? data.empty : false
        };
    }

    /**
     * Fetch AWS connectors from Qualys CloudView API.
     * 
     * @param page - Page number (0-indexed)
     * @param pageSize - Number of items per page
     * @returns ConnectorResponse containing list of connectors and pagination info
     * @throws Error if API call fails or response cannot be parsed
     */
    async fetchConnectors(page: number = 0, pageSize: number = 50): Promise<ConnectorResponse> {
        const url = QualysAWSConnector.ENDPOINT;
        const params = {
            pageNo: page,
            pageSize: pageSize
        };

        console.log(`Fetching AWS connectors from ${this.config.baseUrl}${url}`);

        try {
            const response = await this.axiosInstance.get<RawAPIResponse>(url, { params });
            const data = response.data;

            console.log(`Successfully fetched ${(data.content || []).length} connectors`);

            return this.parseResponse(data);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error(`Failed to fetch connectors: ${error.message}`);
                throw new Error(`API request failed: ${error.message}`);
            }
            console.error(`Failed to parse response: ${error}`);
            throw new Error(`Invalid API response format: ${error}`);
        }
    }

    /**
     * Fetch all AWS connectors, handling pagination automatically.
     * 
     * @returns Array of all AWSConnector objects
     */
    async getAllConnectors(): Promise<AWSConnector[]> {
        const allConnectors: AWSConnector[] = [];
        let page = 0;

        while (true) {
            const response = await this.fetchConnectors(page);
            allConnectors.push(...response.connectors);

            if (response.is_last) {
                break;
            }
            page++;
        }

        console.log(`Fetched total of ${allConnectors.length} connectors`);
        return allConnectors;
    }

    /**
     * Find a specific connector by its ID.
     * 
     * @param connectorId - The connector UUID to search for
     * @returns AWSConnector if found, undefined otherwise
     */
    async getConnectorById(connectorId: string): Promise<AWSConnector | undefined> {
        const connectors = await this.getAllConnectors();
        return connectors.find(c => c.connector_id === connectorId);
    }

    /**
     * Convert connector to normalized dictionary format.
     * 
     * This uses the BASELINE SCHEMA field names (snake_case) which differ
     * from the actual API response (camelCase). CARE should detect this mismatch.
     */
    toNormalizedDict(connector: AWSConnector): Record<string, any> {
        return {
            name: connector.name,
            connector_id: connector.connector_id,  // Should be 'connectorId'
            description: connector.description,
            provider: connector.provider,
            status: connector.status,  // Should be 'state'
            total_assets: connector.total_assets,  // Should be 'totalAssets'
            last_synced_on: connector.last_synced_on,  // Should be 'lastSyncedOn'
            is_gov_cloud: connector.is_gov_cloud,  // Should be 'isGovCloud'
            is_china_region: connector.is_china_region,  // Should be 'isChinaRegion'
            aws_account_id: connector.aws_account_id,  // Should be 'awsAccountId'
            is_disabled: connector.is_disabled,  // Should be 'isDisabled'
            polling_frequency: {  // Should be 'pollingFrequency'
                hours: connector.polling_frequency.hours,
                minutes: connector.polling_frequency.minutes
            },
            error: connector.error,
            base_account_id: connector.base_account_id,  // Should be 'baseAccountId'
            external_id: connector.external_id,  // Should be 'externalId'
            arn: connector.arn
            // MISSING: nextSyncedOn, remediationEnabled, qualysTags, portalConnectorUuid, isPortalConnector
        };
    }
}
