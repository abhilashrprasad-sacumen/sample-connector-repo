import requests
        from typing import List, Optional

        class PollingFrequency:
            def __init__(self, hours: int, minutes: int):
                self.hours = hours
                self.minutes = minutes

        class AWSConnector:
            def __init__(self, name: str, connector_id: str, description: str, provider: str, status: str,
                         total_assets: int, last_synced_on: str, is_gov_cloud: bool, is_china_region: bool,
                         aws_account_id: str, is_disabled: bool, polling_frequency: PollingFrequency, error: str,
                         base_account_id: str, external_id: str, arn: str):
                self.name = name
                self.connector_id = connector_id
                self.description = description
                self.provider = provider
                self.status = status
                self.total_assets = total_assets
                self.last_synced_on = last_synced_on
                self.is_gov_cloud = is_gov_cloud
                self.is_china_region = is_china_region
                self.aws_account_id = aws_account_id
                self.is_disabled = is_disabled
                self.polling_frequency = polling_frequency
                self.error = error
                self.base_account_id = base_account_id
                self.external_id = external_id
                self.arn = arn

        class PaginationInfo:
            def __init__(self, page_number: int, page_size: int, total_pages: int, total_elements: int,
                         number_of_elements: int):
                self.page_number = page_number
                self.page_size = page_size
                self.total_pages = total_pages
                self.total_elements = total_elements
                self.number_of_elements = number_of_elements

        class ConnectorResponse:
            def __init__(self, connectors: List[AWSConnector], pagination: PaginationInfo,
                         is_first: bool, is_last: bool, is_empty: bool):
                self.connectors = connectors
                self.pagination = pagination
                self.is_first = is_first
                self.is_last = is_last
                self.is_empty = is_empty

        class QualysAWSConnector:
            def __init__(self, username: str = None, password: str = None, timeout: int = 30):
                self.username = username or os.getenv('QUALYS_USERNAME')
                self.password = password or os.getenv('QUALYS_PASSWORD')
                self.timeout = timeout
                self.base_url = "https://qualysapi.qualys.com/msp/v1"

            def _build_auth_header(self) -> dict:
                return {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Authorization': f'Basic {base64.b64encode(f"{self.username}:{self.password}".encode()).decode()}'
                }

            def fetch_connectors(self, page: int = 0, page_size: int = 50) -> ConnectorResponse:
                url = f"{self.base_url}/connector"
                params = {
                    "pageNo": page,
                    "pageSize": page_size
                }
                headers = self._build_auth_header()

                try:
                    response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
                    response.raise_for_status()
                    data = response.json()
                    content = data.get("content", [])
                    connectors = [self._parse_connector(c) for c in content]
                    pagination = self._parse_pagination(data)
                    return ConnectorResponse(connectors=connectors, pagination=pagination,
                                             is_first=data.get("first", True),
                                             is_last=data.get("last", True),
                                             is_empty=data.get("empty", False))
                except requests.RequestException as e:
                    raise ValueError(f"Failed to fetch connectors: {e}")

            def _parse_connector(self, data: dict) -> AWSConnector:
                polling_frequency = PollingFrequency(hours=data.get("pollingFrequency", {}).get("hours", 0),
                                                     minutes=data.get("pollingFrequency", {}).get("minutes", 0))
                return AWSConnector(
                    name=data.get("name"),
                    connector_id=data.get("id"),
                    description=data.get("description"),
                    provider=data.get("provider"),
                    status=data.get("status"),
                    total_assets=data.get("totalAssets"),
                    last_synced_on=data.get("lastSyncedOn"),
                    is_gov_cloud=data.get("isGovCloud"),
                    is_china_region=data.get("isChinaRegion"),
                    aws_account_id=data.get("awsAccountId"),
                    is_disabled=data.get("isDisabled"),
                    polling_frequency=polling_frequency,
                    error=data.get("error"),
                    base_account_id=data.get("baseAccountId"),
                    external_id=data.get("externalId"),
                    arn=data.get("arn")
                )

            def _parse_pagination(self, data: dict) -> PaginationInfo:
                pageable = data.get("pageable", {})
                return PaginationInfo(
                    page_number=pageable.get("pageNumber", 0),
                    page_size=pageable.get("pageSize", 50),
                    total_pages=data.get("totalPages", 1),
                    total_elements=data.get("totalElements", 0),
                    number_of_elements=data.get("numberOfElements", 0)
                )

            def get_all_connectors(self) -> List[AWSConnector]:
                all_connectors = []
                page = 0
                while True:
                    response = self.fetch_connectors(page=page)
                    all_connectors.extend(response.connectors)
                    if response.is_last:
                        break
                    page += 1
                return all_connectors

            def get_connector_by_id(self, connector_id: str) -> Optional[AWSConnector]:
                connectors = self.get_all_connectors()
                for connector in connectors:
                    if connector.connector_id == connector_id:
                        return connector
                return None

            def to_normalized_dict(self, connector: AWSConnector) -> dict:
                return {
                    "name": connector.name,
                    "connector_id": connector.connector_id,
                    "description": connector.description,
                    "provider": connector.provider,
                    "status": connector.status,
                    "total_assets": connector.total_assets,
                    "last_synced_on": connector.last_synced_on,
                    "is_gov_cloud": connector.is_gov_cloud,
                    "is_china_region": connector.is_china_region,
                    "aws_account_id": connector.aws_account_id,
                    "is_disabled": connector.is_disabled,
                    "polling_frequency": {
                        "hours": connector.polling_frequency.hours,
                        "minutes": connector.polling_frequency.minutes
                    },
                    "error": connector.error,
                    "base_account_id": connector.base_account_id,
                    "external_id": connector.external_id,
                    "arn": connector.arn
                }

        def main():
            try:
                connector = QualysAWSConnector()
                response = connector.fetch_connectors()
                print(f"Total Connectors: {response.pagination.total_elements}")
                for conn in response.connectors:
                    print(f"Name: {conn.name}, Connector ID: {conn.connector_id}, Status: {conn.status}")
            except ValueError as e:
                print(f"Configuration error: {e}")

        if __name__ == "__main__":
            main()