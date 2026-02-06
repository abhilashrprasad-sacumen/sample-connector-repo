/**
 * Main entry point for the Qualys AWS Connector.
 * Demonstrates connector usage and displays fetched connector information.
 */

import { QualysAWSConnector } from './connector';

/**
 * Main function to demonstrate connector usage.
 */
async function main(): Promise<void> {
    try {
        // Initialize connector (will use environment variables for auth)
        const connector = new QualysAWSConnector();

        // Fetch connectors
        const response = await connector.fetchConnectors();

        console.log('\n' + '='.repeat(60));
        console.log('QUALYS AWS CONNECTORS');
        console.log('='.repeat(60));
        console.log(`Total Connectors: ${response.pagination.total_elements}`);
        console.log(`Page: ${response.pagination.page_number + 1} of ${response.pagination.total_pages}`);
        console.log('='.repeat(60) + '\n');

        for (const conn of response.connectors) {
            console.log(`Name: ${conn.name}`);
            console.log(`  Connector ID: ${conn.connector_id}`);
            console.log(`  Provider: ${conn.provider}`);
            console.log(`  Status: ${conn.status}`);  // Using 'status' but actual field is 'state'
            console.log(`  Total Assets: ${conn.total_assets}`);
            console.log(`  AWS Account ID: ${conn.aws_account_id}`);
            console.log(`  Last Synced: ${conn.last_synced_on}`);
            console.log(`  Is Disabled: ${conn.is_disabled}`);
            console.log(`  ARN: ${conn.arn}`);
            console.log();
        }

        // Export as normalized dict (using baseline schema field names)
        console.log('\n' + '='.repeat(60));
        console.log('NORMALIZED OUTPUT (Baseline Schema Format)');
        console.log('='.repeat(60));
        for (const conn of response.connectors) {
            const normalized = connector.toNormalizedDict(conn);
            console.log(JSON.stringify(normalized, null, 2));
        }

    } catch (error) {
        if (error instanceof Error) {
            console.error(`\nError: ${error.message}`);

            if (error.message.includes('environment variables')) {
                console.log('\nPlease set the following environment variables:');
                console.log("  export QUALYS_USERNAME='your_username'");
                console.log("  export QUALYS_PASSWORD='your_password'");
            }
        } else {
            console.error('An unexpected error occurred:', error);
        }
        process.exit(1);
    }
}

// Run main function
main();
