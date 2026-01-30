# Qualys AWS Connector - CARE Test Repository

This repository contains a sample connector for the Qualys CloudView AWS Connectors API, designed specifically for testing **CARE (Connector Auto-Repair Engine)**.

## Purpose

The connector intentionally uses an **OUTDATED baseline schema** that differs from the actual API response. When CARE monitors this connector and compares it against the live API, it will detect schema changes and auto-correct the code.

## Files

```
src/
├── connector.py          # Main connector with intentional schema mismatches (366 lines)
├── auth_config.py        # Authentication configuration module with env var support
├── baseline_schema.json  # Outdated schema for CARE comparison (81 lines)
├── requirements.txt      # Python dependencies (requests, python-dotenv)
└── .env                  # Environment variables configuration
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

1. Install dependencies:
   ```bash
   cd src
   pip install -r requirements.txt
   ```

2. Configure credentials in `.env`:
   ```bash
   # Edit src/.env with your Qualys credentials
   QUALYS_BASE_URL=https://qualysguard.qg2.apps.qualys.eu
   QUALYS_USERNAME=your_username
   QUALYS_PASSWORD=your_password
   QUALYS_TIMEOUT=30
   QUALYS_VERIFY_SSL=true
   ```

3. Or set environment variables directly:
   ```bash
   export QUALYS_USERNAME='your_username'
   export QUALYS_PASSWORD='your_password'
   ```

## Usage

```python
from connector import QualysAWSConnector

# Initialize connector
connector = QualysAWSConnector()

# Fetch connectors
response = connector.fetch_connectors()

# Access connector data
for conn in response.connectors:
    print(f"Name: {conn.name}")
    print(f"Status: {conn.status}")  # Note: Uses 'status' but API returns 'state'
```

## CARE Testing Workflow

1. CARE monitors the endpoint: `https://qualysguard.qg2.apps.qualys.eu/cloudview-api/rest/v1/aws/connectors`
2. CARE compares the actual API response against `baseline_schema.json`
3. CARE detects the schema differences (field naming, missing fields, renamed fields)
4. CARE generates patches to auto-correct `connector.py`:
   - Update field mappings from snake_case to camelCase
   - Change `status` to `state`
   - Add missing fields: `nextSyncedOn`, `remediationEnabled`, `qualysTags`, `portalConnectorUuid`, `isPortalConnector`

## API Endpoint

**URL:** `https://qualysguard.qg2.apps.qualys.eu/cloudview-api/rest/v1/aws/connectors`  
**Auth:** Basic Authentication  
**Method:** GET
