def _parse_connector(self, c: Dict[str, Any]) -> AWSConnector:
        """Parse individual connector from API response."""
        return AWSConnector(
            name=c.get('name', ''),
            connectorId=c.get('connectorId', ''),  # Corrected field name
            description=c.get('description', ''),
            provider=c.get('provider', ''),
            status=c.get('status', ''),  # Corrected field name
            totalAssets=c.get('totalAssets', 0),  # Corrected field name
            lastSyncedOn=c.get('lastSyncedOn', ''),  # Corrected field name
            isGovCloud=c.get('isGovCloud', False),  # Corrected field name
            isChinaRegion=c.get('isChinaRegion', False),  # Corrected field name
            awsAccountId=c.get('awsAccountId', ''),  # Corrected field name
            isDisabled=c.get('isDisabled', False),  # Corrected field name
            pollingFrequency=PollingFrequency(
                hours=c.get('pollingFrequency', {}).get('hours', 0),
                minutes=c.get('pollingFrequency', {}).get('minutes', 0)
            ),
            error=c.get('error', ''),
            baseAccountId=c.get('baseAccountId', ''),  # Corrected field name
            externalId=c.get('externalId', ''),  # Corrected field name
            arn=c.get('arn', '')
        )

    def _parse_response(self, data: Dict[str, Any]) -> ConnectorResponse:
        """Parse full API response into ConnectorResponse object."""
        content = data.get('content', [])
        connectors = [self._parse_connector(c) for c in content]
        pagination = self._parse_pagination(data)
        
        return ConnectorResponse(
            connectors=connectors,
            pagination=pagination,
            isFirst=data.get('first', True),
            isLast=data.get('last', True),
            isEmpty=data.get('empty', False)
        )