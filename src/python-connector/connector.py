class ConnectorResponse:
    def __init__(self, connectors, pagination, is_first, is_last, is_empty):
        self.connectors = connectors
        self.pagination = pagination
        self.is_first = is_first
        self.is_last = is_last
        self.is_empty = is_empty


def _parse_connector(self, c):
    return AWSConnector(
        name=c['name'],
        connector_id=c['connectorId'],
        description=c.get('description', ''),
        provider=c['provider'],
        status=c['status'],
        total_assets=c['totalAssets'],
        last_synced_on=c.get('lastSyncedOn', None),
        is_gov_cloud=c.get('isGovCloud', False),
        is_china_region=c.get('isChinaRegion', False),
        aws_account_id=c['awsAccountId'],
        is_disabled=c.get('isDisabled', False),
        polling_frequency=PollingFrequency(
            hours=c['pollingFrequency']['hours'],
            minutes=c['pollingFrequency']['minutes']
        ),
        error=c.get('error', ''),
        base_account_id=c['baseAccountId'],
        external_id=c['externalId'],
        arn=c['arn'],
        next_synced_on=c.get('nextSyncedOn', None),
        remediation_enabled=c.get('remediationEnabled', False),
        qualys_tags=c.get('qualysTags', []),
        portal_connector_uuid=c.get('portalConnectorUuid', ''),
        is_portal_connector=c.get('isPortalConnector', False)
    )