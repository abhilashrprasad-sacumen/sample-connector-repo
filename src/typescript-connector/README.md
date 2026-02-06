# Qualys AWS Connector - TypeScript Implementation

This is a TypeScript implementation of the Qualys CloudView AWS Connectors API connector, designed specifically for testing **CARE (Connector Auto-Repair Engine)**.

## Purpose

The connector intentionally uses an **OUTDATED baseline schema** that differs from the actual API response. When CARE monitors this connector and compares it against the live API, it will detect schema changes and auto-correct the code.

## Files

```
src/typescript-connector/
├── src/
│   ├── authConfig.ts      # Authentication configuration with env var support
│   ├── types.ts           # TypeScript interfaces with intentional schema mismatches
│   ├── connector.ts       # Main connector class (mirrors Python version)
│   └── index.ts           # Entry point demonstrating usage
├── baseline_schema.json   # Outdated schema for CARE comparison
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Intentional Schema Differences

The baseline schema has the following intentional differences from the actual Qualys API:

### Field Naming (snake_case → camelCase)
| Baseline Schema | Actual API |
|-----------------|------------|
| `connector_id` | `connectorId` |
| `total_assets` | `totalAssets` |
| `last_synced_on` | `lastSyncedOn` |
| `is_gov_cloud` | `isGovCloud` |
| `is_china_region` | `isChinaRegion` |
| `aws_account_id` | `awsAccountId` |
| `is_disabled` | `isDisabled` |
| `polling_frequency` | `pollingFrequency` |
| `base_account_id` | `baseAccountId` |
| `external_id` | `externalId` |
| `page_number` | `pageNumber` |
| `page_size` | `pageSize` |
| `total_pages` | `totalPages` |
| `total_elements` | `totalElements` |
| `number_of_elements` | `numberOfElements` |

### Renamed Fields
| Baseline Schema | Actual API |
|-----------------|------------|
| `status` | `state` |

### Missing Fields (New in Actual API)
- `nextSyncedOn`
- `remediationEnabled`
- `qualysTags`
- `portalConnectorUuid`
- `isPortalConnector`

## Setup

1. **Install dependencies:**
   ```bash
   cd src/typescript-connector
   npm install
   ```

2. **Configure credentials in `.env`:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your Qualys credentials
   QUALYS_BASE_URL=https://qualysguard.qg2.apps.qualys.eu
   QUALYS_USERNAME=your_username
   QUALYS_PASSWORD=your_password
   QUALYS_TIMEOUT=30
   QUALYS_VERIFY_SSL=true
   ```

3. **Or set environment variables directly:**
   ```bash
   export QUALYS_USERNAME='your_username'
   export QUALYS_PASSWORD='your_password'
   ```

## Usage

### Build and Run

```bash
# Build TypeScript to JavaScript
npm run build

# Run the compiled code
npm start

# Or run directly with ts-node (development)
npm run dev
```

### Programmatic Usage

```typescript
import { QualysAWSConnector } from './connector';

// Initialize connector
const connector = new QualysAWSConnector();

// Fetch connectors
const response = await connector.fetchConnectors();

// Access connector data
for (const conn of response.connectors) {
  console.log(`Name: ${conn.name}`);
  console.log(`Status: ${conn.status}`);  // Note: Uses 'status' but API returns 'state'
}

// Get all connectors (handles pagination)
const allConnectors = await connector.getAllConnectors();

// Find specific connector by ID
const connector = await connector.getConnectorById('some-uuid');

// Export as normalized dictionary
const normalized = connector.toNormalizedDict(conn);
```

## CARE Testing Workflow

1. CARE monitors the endpoint: `https://qualysguard.qg2.apps.qualys.eu/cloudview-api/rest/v1/aws/connectors`
2. CARE compares the actual API response against `baseline_schema.json`
3. CARE detects the schema differences (field naming, missing fields, renamed fields)
4. CARE generates patches to auto-correct the TypeScript code:
   - Update field mappings from snake_case to camelCase
   - Change `status` to `state`
   - Add missing fields: `nextSyncedOn`, `remediationEnabled`, `qualysTags`, `portalConnectorUuid`, `isPortalConnector`

## API Endpoint

**URL:** `https://qualysguard.qg2.apps.qualys.eu/cloudview-api/rest/v1/aws/connectors`  
**Auth:** Basic Authentication  
**Method:** GET

## TypeScript Features

- **Strict Type Checking**: Full TypeScript strict mode enabled
- **Async/Await**: Modern asynchronous programming
- **Axios**: Robust HTTP client with interceptors
- **Environment Variables**: Secure credential management with dotenv
- **Error Handling**: Comprehensive error handling and validation

## Comparison with Python Version

This TypeScript implementation mirrors the Python connector's functionality:
- Same intentional schema mismatches
- Same authentication mechanism (Basic Auth)
- Same pagination handling
- Same field mapping logic with fallbacks
- Same normalized output format
