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
        description=c['description'],
        provider=c['provider'],
        status=c['status'],
        total_assets=c['totalAssets'],
        last_synced_on=c['lastSyncedOn'],
        is_gov_cloud=c['isGovCloud'],
        is_china_region=c['isChinaRegion'],
        aws_account_id=c['awsAccountId'],
        is_disabled=c['isDisabled'],
        polling_frequency=PollingFrequency(
            hours=c['pollingFrequency']['hours'],
            minutes=c['pollingFrequency']['minutes']
        ),
        error=c['error'],
        base_account_id=c['baseAccountId'],
        external_id=c['externalId'],
        arn=c['arn'],
        next_synced_on=c.get('nextSyncedOn'),  # Added
        remediation_enabled=c.get('remediationEnabled'),  # Added
        qualys_tags=c.get('qualysTags'),  # Added
        portal_connector_uuid=c.get('portalConnectorUuid'),  # Added
        is_portal_connector=c.get('isPortalConnector')  # Added
    )

def fetch_connectors(self, page=0, page_size=50):
    url = self._build_url(self.ENDPOINT)
    params = {
        "pageNo": page,
        "pageSize": page_size
    }

    logger.info(f"Fetching AWS connectors from {url}")

    try:
        response = self.session.get(
            url,
            params=params,
            timeout=self.config.timeout
        )
        response.raise_for_status()

        data = response.json()
        logger.info(f"Successfully fetched {len(data.get('content', []))} connectors")

        return self._parse_response(data)

    except requests.RequestException as e:
        logger.error(f"Failed to fetch connectors: {e}")
        raise
    except (KeyError, ValueError) as e:
        logger.error(f"Failed to parse response: {e}")
        raise ValueError(f"Invalid API response format: {e}")

def _parse_response(self, data):
    content = data.get('content', [])
    connectors = [self._parse_connector(c) for c in content]
    pagination = self._parse_pagination(data)

    return ConnectorResponse(
        connectors=connectors,
        pagination=pagination,
        is_first=data.get("first", True),
        is_last=data.get("last", True),
        is_empty=data.get("empty", False)
    )