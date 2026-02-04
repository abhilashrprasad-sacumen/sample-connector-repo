python
""
Qualys AWS Connectors API Connector

This connector fetches AWS connector information from the Qualys CloudView API.

IMPORTANT: This connector uses an OUTDATED baseline schema with intentional differences
from the actual API response. This is designed for testing of automatic schema change detection and code patching.
""

import requests
from dataclasses import dataclass, field
from typing import List, Optional
class PollingFrequency:
    hours: int
def normalize_date(date_str):
    return date_str.replace('T', ' ').split('.')[0]
@dataclass
class AWSConnector:
    name: str
def parse_connector(connector_data):
    return AWSConnector(
        name=connector_data['name'],
        # Add other fields as needed
    )
def fetch_connectors(page: int = 0, page_size: int = 50) -> List[AWSConnector]:
    url = 'https://api.qualys.com/v2.0/asset/aws_connector'
    params = {
        'pageNo': page,
        'pageSize': page_size
    }
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': f'Basic {base64.b64encode(f'{os.getenv("QUALYS_USERNAME")}:{os.getenv("QUALYS_PASSWORD")}'.encode()).decode()}'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return [parse_connector(conn) for conn in data['content']]
    else:
        raise Exception(f'Failed to fetch connectors: {response.status_code}')
def main():
    try:
        connectors = fetch_connectors()
        for connector in connectors:
            print(f'Name: {connector.name}')
    except Exception as e:
        print(f'Error: {e}')
if __name__ == '__main__':
    main()
