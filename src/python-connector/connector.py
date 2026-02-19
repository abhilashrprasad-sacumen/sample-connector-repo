class AWSConnector:
        # ... (other code remains unchanged)

        def _parse_connector(self, c):
            return AWSConnector(
                name=c.get('name', ''),
                connector_id=c.get('connectorId', ''),  # Updated field name
                description=c.get('description', ''),
                provider=c.get('provider', ''),
                status=c.get('state', ''),  # Updated field name
                total_assets=c.get('totalAssets', 0),  # Updated field name
                last_synced_on=c.get('lastSyncedOn', ''),  # Updated field name
                is_gov_cloud=c.get('isGovCloud', False),  # Updated field name
                is_china_region=c.get('isChinaRegion', False),  # Updated field name
                aws_account_id=c.get('awsAccountId', ''),  # Updated field name
                is_disabled=c.get('isDisabled', False),  # Updated field name
                polling_frequency=PollingFrequency(
                    hours=c.get('pollingFrequency', {}).get('hours', 0),
                    minutes=c.get('pollingFrequency', {}).get('minutes', 0)
                ),
                error=c.get('error', ''),
                base_account_id=c.get('baseAccountId', ''),  # Updated field name
                external_id=c.get('externalId', ''),  # Updated field name
                arn=c.get('arn', '')
            )

        def _parse_response(self, data):
            content = data.get('content', [])
            connectors = [self._parse_connector(c) for c in content]
            pagination = self._parse_pagination(data)
            return ConnectorResponse(
                connectors=connectors,
                pagination=pagination,
                is_first=data.get('first', True),
                is_last=data.get('last', True),
                is_empty=data.get('empty', False)
            )

        def to_normalized_dict(self, connector):
            return {
                "name": connector.name,
                "connector_id": connector.connector_id,  # Updated field name
                "description": connector.description,
                "provider": connector.provider,
                "status": connector.status,  # Updated field name
                "total_assets": connector.total_assets,  # Updated field name
                "last_synced_on": connector.last_synced_on,  # Updated field name
                "is_gov_cloud": connector.is_gov_cloud,  # Updated field name
                "is_china_region": connector.is_china_region,  # Updated field name
                "aws_account_id": connector.aws_account_id,  # Updated field name
                "is_disabled": connector.is_disabled,  # Updated field name
                "polling_frequency": {
                    "hours": connector.polling_frequency.hours,
                    "minutes": connector.polling_frequency.minutes
                },
                "error": connector.error,
                "base_account_id": connector.base_account_id,  # Updated field name
                "external_id": connector.external_id,  # Updated field name
                "arn": connector.arn
            }

    def main():
        try:
            connector = QualysAWSConnector()
            response = connector.fetch_connectors()

            print(f"\n{'='*60}")
            print("QUALYS AWS CONNECTORS")
            print(f"{'='*60}")
            print(f"Total Connectors: {response.pagination.total_elements}")
            print(f"Page: {response.pagination.page_number + 1} of {response.pagination.total_pages}")
            print(f"{'='*60}\n")

            for conn in response.connectors:
                print(f"Name: {conn.name}")
                print(f"  Connector ID: {conn.connector_id}")
                print(f"  Provider: {conn.provider}")
                print(f"  Status: {conn.status}")  # Using 'status' but actual field is 'state'
                print(f"  Total Assets: {conn.total_assets}")
                print(f"  AWS Account ID: {conn.aws_account_id}")
                print(f"  Last Synced: {conn.last_synced_on}")
                print(f"  Is Disabled: {conn.is_disabled}")
                print(f"  ARN: {conn.arn}")
                print()

            print(f"\n{'='*60}")
            print("NORMALIZED OUTPUT (Baseline Schema Format)")
            print(f"{'='*60}")
            for conn in response.connectors:
                normalized = connector.to_normalized_dict(conn)
                print(json.dumps(normalized, indent=2))

        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            print(f"\nError: {e}")
            print("\nPlease set the following environment variables:")
            print("  export QUALYS_USERNAME='your_username'")
            print("  export QUALYS_PASSWORD='your_password'")
        except requests.RequestException as e:
            logger.error(f"API error: {e}")

    if __name__ == "__main__":
        main()