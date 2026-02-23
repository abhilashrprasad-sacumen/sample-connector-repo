class QualysAWSConnector:
    # ... (other methods remain unchanged)

    def _parse_connector(self, c: Dict[str, Any]) -> AWSConnector:
        return AWSConnector(
            name=c.get("name", ""),
            connector_id=c.get("connectorId", ""),  # Corrected field name
            description=c.get("description", ""),
            provider=c.get("provider", ""),
            status=c.get("status", ""),  # Corrected field name
            total_assets=c.get("totalAssets", 0),  # Corrected field name
            last_synced_on=c.get("lastSyncedOn", ""),  # Corrected field name
            is_gov_cloud=c.get("isGovCloud", False),  # Corrected field name
            is_china_region=c.get("isChinaRegion", False),  # Corrected field name
            aws_account_id=c.get("awsAccountId", ""),  # Corrected field name
            is_disabled=c.get("isDisabled", False),  # Corrected field name
            polling_frequency=PollingFrequency(
                hours=c.get("pollingFrequency", {}).get("hours", 0),
                minutes=c.get("pollingFrequency", {}).get("minutes", 0)
            ),
            error=c.get("error", ""),
            base_account_id=c.get("baseAccountId", ""),  # Corrected field name
            external_id=c.get("externalId", ""),  # Corrected field name
            arn=c.get("arn", "")
        )

    def _parse_pagination(self, data: Dict[str, Any]) -> PaginationInfo:
        pageable = data.get("pageable", {})
        return PaginationInfo(
            page_number=pageable.get("pageNumber", 0),
            page_size=pageable.get("pageSize", 50),  # Corrected field name
            total_pages=data.get("totalPages", 0),
            total_elements=data.get("totalElements", 0),
            number_of_elements=data.get("numberOfElements", 0)
        )

    def fetch_connectors(self, page: int = 0, page_size: int = 50) -> ConnectorResponse:
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

    def _parse_response(self, data: Dict[str, Any]) -> ConnectorResponse:
        content = data.get("content", [])
        connectors = [self._parse_connector(c) for c in content]
        pagination = self._parse_pagination(data)
        
        return ConnectorResponse(
            connectors=connectors,
            pagination=pagination,
            is_first=data.get("first", True),
            is_last=data.get("last", True),
            is_empty=data.get("empty", False)
        )

    # ... (other methods remain unchanged)

if __name__ == "__main__":
    main()