/**
 * Authentication configuration for Qualys API connector.
 * Uses Basic Authentication with username and password.
 */

import * as dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

/**
 * Configuration interface for Qualys API authentication.
 */
export interface QualysAuthConfig {
    /** Base URL for the Qualys API */
    baseUrl: string;
    /** API username */
    username: string;
    /** API password */
    password: string;
    /** Request timeout in seconds */
    timeout: number;
    /** Whether to verify SSL certificates */
    verifySsl: boolean;
}

/**
 * Load authentication configuration from environment variables.
 * 
 * Expected environment variables:
 * - QUALYS_BASE_URL: Base URL for Qualys API (optional, has default)
 * - QUALYS_USERNAME: API username (required)
 * - QUALYS_PASSWORD: API password (required)
 * - QUALYS_TIMEOUT: Request timeout in seconds (optional)
 * - QUALYS_VERIFY_SSL: Whether to verify SSL certificates (optional)
 * 
 * @returns QualysAuthConfig object
 */
export function loadAuthConfig(): QualysAuthConfig {
    return {
        baseUrl: process.env.QUALYS_BASE_URL || 'https://qualysguard.qg2.apps.qualys.eu',
        username: process.env.QUALYS_USERNAME || '',
        password: process.env.QUALYS_PASSWORD || '',
        timeout: parseInt(process.env.QUALYS_TIMEOUT || '30', 10),
        verifySsl: (process.env.QUALYS_VERIFY_SSL || 'true').toLowerCase() === 'true'
    };
}

/**
 * Validate that required credentials are provided.
 * 
 * @param config - The authentication configuration to validate
 * @throws Error if username or password is missing
 */
export function validateAuthConfig(config: QualysAuthConfig): void {
    if (!config.username || !config.password) {
        throw new Error('QUALYS_USERNAME and QUALYS_PASSWORD environment variables must be set');
    }
}

/**
 * Get Basic Authentication header value.
 * 
 * @param config - The authentication configuration
 * @returns Base64-encoded Basic Auth string
 */
export function getAuthHeader(config: QualysAuthConfig): string {
    const credentials = `${config.username}:${config.password}`;
    return `Basic ${Buffer.from(credentials).toString('base64')}`;
}

/** Default configuration instance loaded from environment variables */
export const defaultConfig: QualysAuthConfig = loadAuthConfig();
