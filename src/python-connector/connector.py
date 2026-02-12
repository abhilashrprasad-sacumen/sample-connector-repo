def _parse_connector(self, c: Dict[str, Any]) -> AWSConnector:
        """Parse individual connector from API response."""
        return AWSConnector(
            name=c.get("name", ""),
            connector_id=c.get("connectorId", ""),  # Updated field name
            description=c.get("description", ""),
            provider=c.get("provider", ""),
            status=c.get("state", ""),  # Updated field name
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

    def to_normalized_dict(self, connector: AWSConnector) -> Dict[str, Any]:
        """Convert connector to normalized dictionary format."""
        return {
            "name": connector.name,
            "connector_id": connector.connector_id,  # Should be 'connectorId'
            "description": connector.description,
            "provider": connector.provider,
            "status": connector.status,  # Should be 'state'
            "total_assets": connector.total_assets,  # Should be 'totalAssets'
            "last_synced_on": connector.last_synced_on,  # Should be 'lastSyncedOn'
            "is_gov_cloud": connector.is_gov_cloud,  # Should be 'isGovCloud'
            "is_china_region": connector.is_china_region,  # Should be 'isChinaRegion'
            "aws_account_id": connector.aws_account_id,  # Should be 'awsAccountId'
            "is_disabled": connector.is_disabled,  # Should be 'isDisabled'
            "polling_frequency": {  # Should be 'pollingFrequency'
                "hours": connector.polling_frequency.hours,
                "minutes": connector.polling_frequency.minutes
            },
            "error": connector.error,
            "base_account_id": connector.base_account_id,  # Should be 'baseAccountId'
            "external_id": connector.external_id,  # Should be 'externalId'
            "arn": connector.arn,
            "nextSyncedOn": connector.next_synced_on,  # Added field
            "remediationEnabled": connector.remediation_enabled,  # Added field
            "qualysTags": connector.qualys_tags,  # Added field
            "portalConnectorUuid": connector.portal_connector_uuid,  # Added field
            "isPortalConnector": connector.is_portal_connector  # Added field
        }