def _parse_connector(self, c: Dict[str, Any]) -> AWSConnector:
        """Parse individual connector from API response."""
        return AWSConnector(
            name=c.get("name", ""),
            connector_id=c.get("connectorId", ""),  # Updated field name
            description=c.get("description", ""),
            provider=c.get("provider", ""),
            status=c.get("status", ""),  # Updated field name
            total_assets=c.get("totalAssets", 0),  # Updated field name
            last_synced_on=c.get("lastSyncedOn", ""),  # Updated field name
            is_gov_cloud=c.get("isGovCloud", False),  # Updated field name
            is_china_region=c.get("isChinaRegion", False),  # Updated field name
            aws_account_id=c.get("awsAccountId", ""),  # Updated field name
            is_disabled=c.get("isDisabled", False),  # Updated field name
            polling_frequency=PollingFrequency(
                hours=c.get("pollingFrequency", {}).get("hours", 0),
                minutes=c.get("pollingFrequency", {}).get("minutes", 0)
            ),
            error=c.get("error", ""),
            base_account_id=c.get("baseAccountId", ""),  # Updated field name
            external_id=c.get("externalId", ""),  # Updated field name
            arn=c.get("arn", "")
        )

    def _parse_pagination(self, data: Dict[str, Any]) -> PaginationInfo:
        """Parse pagination information from API response."""
        pageable = data.get("pageable", {})
        return PaginationInfo(
            page_number=pageable.get("pageNumber", 0),
            page_size=pageable.get("pageSize", 50),
            total_pages=data.get("totalPages", 0),
            total_elements=data.get("totalElements", 0),
            number_of_elements=data.get("numberOfElements", 0)
        )

    def to_normalized_dict(self, connector: AWSConnector) -> Dict[str, Any]:
        """Convert connector to normalized dictionary format."""
        return {
            "name": connector.name,
            "connectorId": connector.connector_id,  # Updated field name
            "description": connector.description,
            "provider": connector.provider,
            "status": connector.status,  # Updated field name
            "totalAssets": connector.total_assets,  # Updated field name
            "lastSyncedOn": connector.last_synced_on,  # Updated field name
            "isGovCloud": connector.is_gov_cloud,  # Updated field name
            "isChinaRegion": connector.is_china_region,  # Updated field name
            "awsAccountId": connector.aws_account_id,  # Updated field name
            "isDisabled": connector.is_disabled,  # Updated field name
            "pollingFrequency": {
                "hours": connector.polling_frequency.hours,
                "minutes": connector.polling_frequency.minutes
            },
            "error": connector.error,
            "baseAccountId": connector.base_account_id,  # Updated field name
            "externalId": connector.external_id,  # Updated field name
            "arn": connector.arn
        }