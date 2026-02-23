class AWSConnector:
    def __init__(self, name, connector_id, description, provider, status, total_assets, last_synced_on, is_gov_cloud, is_china_region, aws_account_id, is_disabled, polling_frequency, error, base_account_id, external_id, arn, nextSyncedOn=None, remediationEnabled=None, qualysTags=None, portalConnectorUuid=None, isPortalConnector=False):
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
        self.nextSyncedOn = nextSyncedOn
        self.remediationEnabled = remediationEnabled
        self.qualysTags = qualysTags
        self.portalConnectorUuid = portalConnectorUuid
        self.isPortalConnector = isPortalConnector

class QualysAWSConnector:
    def _parse_connector(self, c):
        return AWSConnector(
            name=c.get('name'),
            connector_id=c.get('id'),
            description=c.get('description'),
            provider=c.get('provider'),
            status=c.get('status'),
            total_assets=c.get('totalAssets'),
            last_synced_on=c.get('lastSyncedOn'),
            is_gov_cloud=c.get('isGovCloud'),
            is_china_region=c.get('isChinaRegion'),
            aws_account_id=c.get('awsAccountId'),
            is_disabled=c.get('isDisabled'),
            polling_frequency={'hours': c.get('pollingFrequency', {}).get('hours'), 'minutes': c.get('pollingFrequency', {}).get('minutes')},
            error=c.get('error'),
            base_account_id=c.get('baseAccountId'),
            external_id=c.get('externalId'),
            arn=c.get('arn'),
            nextSyncedOn=c.get('nextSyncedOn'),
            remediationEnabled=c.get('remediationEnabled'),
            qualysTags=c.get('qualysTags'),
            portalConnectorUuid=c.get('portalConnectorUuid'),
            isPortalConnector=c.get('isPortalConnector', False)
        )

    def to_normalized_dict(self, connector):
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
                "hours": connector.polling_frequency['hours'],
                "minutes": connector.polling_frequency['minutes']
            },
            "error": connector.error,
            "base_account_id": connector.base_account_id,
            "external_id": connector.external_id,
            "arn": connector.arn,
            "nextSyncedOn": connector.nextSyncedOn,
            "remediationEnabled": connector.remediationEnabled,
            "qualysTags": connector.qualysTags,
            "portalConnectorUuid": connector.portalConnectorUuid,
            "isPortalConnector": connector.isPortalConnector
        }

# Rest of the code remains unchanged