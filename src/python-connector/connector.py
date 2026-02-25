diff
@@ -1,4 +1,4 @@
-"""
-Qualys AWS Connectors API Connector
+"""
+"""
 Qualys AWS Connectors API Connector

 This connector fetches AWS connector information from the Qualys CloudView API.
@@ -34,7 +34,7 @@
     name: str
     connector_id: str  # Actual API field: connectorId
     description: str
-    provider: str
+    provider: str
     status: str  # Actual API field: state (RENAMED FIELD)
     total_assets: int  # Actual API field: totalAssets
     last_synced_on: str  # Actual API field: lastSyncedOn
@@ -43,7 +43,7 @@
     is_disabled: bool  # Actual API field: isDisabled
     polling_frequency: PollingFrequency
     error: str
-    base_account_id: str  # Actual API field: baseAccountId
+    base_account_id: str  # Actual API field: baseAccountId
     external_id: str  # Actual API field: externalId
     arn: str
     # MISSING FIELDS from actual API:
@@ -55,7 +55,7 @@
     page_number: int  # Actual API field: pageNumber
     page_size: int  # Actual API field: pageSize
     total_pages: int  # Actual API field: totalPages
-    total_elements: int  # Actual API field: totalElements
+    total_elements: int  # Actual API field: totalElements
     number_of_elements: int  # Actual API field: numberOfElements


@@ -72,7 +72,7 @@
     def _parse_polling_frequency(self, data: Dict[str, Any]) -> PollingFrequency:
         """
         Parse polling frequency from API response.
-
+
         Uses baseline schema field names (snake_case) but actual API returns camelCase.
         """
         # NOTE: Baseline schema expects 'polling_frequency' but API returns 'pollingFrequency'
@@ -80,7 +80,7 @@
         return PollingFrequency(
             hours=freq_data.get("hours", 0),
             minutes=freq_data.get("minutes", 0)
-        )
+        )

     def _parse_connector(self, data: Dict[str, Any]) -> AWSConnector:
         """
@@ -88,14 +88,14 @@
         """
         return AWSConnector(
             name=data.get("name", ""),
-            # Using 'connector_id' but API returns 'connectorId'
-            connector_id=data.get("connector_id", data.get("connectorId", "")),
+            # Using 'connector_id' but API returns 'connectorId'
+            connector_id=data.get("connectorId", ""),
             description=data.get("description", ""),
             provider=data.get("provider", ""),
-            # Using 'status' but API returns 'state' (FIELD RENAMED)
-            status=data.get("status", data.get("state", "")),
+            # Using 'status' but API returns 'state' (FIELD RENAMED)
+            status=data.get("state", ""),
             # Using 'total_assets' but API returns 'totalAssets'
-            total_assets=data.get("total_assets", data.get("totalAssets", 0)),
+            total_assets=data.get("totalAssets", 0),
             # Using 'last_synced_on' but API returns 'lastSyncedOn'
-            last_synced_on=data.get("last_synced_on", data.get("lastSyncedOn", "")),
+            last_synced_on=data.get("lastSyncedOn", ""),
             # Using 'is_gov_cloud' but API returns 'isGovCloud'
-            is_gov_cloud=data.get("is_gov_cloud", data.get("isGovCloud", False)),
+            is_gov_cloud=data.get("isGovCloud", False),
             # Using 'is_china_region' but API returns 'isChinaRegion'
-            is_china_region=data.get("is_china_region", data.get("isChinaRegion", False)),
+            is_china_region=data.get("isChinaRegion", False),
             # Using 'aws_account_id' but API returns 'awsAccountId'
-            aws_account_id=data.get("aws_account_id", data.get("awsAccountId", "")),
+            aws_account_id=data.get("awsAccountId", ""),
             # Using 'is_disabled' but API returns 'isDisabled'
-            is_disabled=data.get("is_disabled", data.get("isDisabled", False)),
+            is_disabled=data.get("isDisabled", False),
             polling_frequency=self._parse_polling_frequency(data),
             error=data.get("error", ""),
             # Using 'base_account_id' but API returns 'baseAccountId'
-            base_account_id=data.get("base_account_id", data.get("baseAccountId", "")),
+            base_account_id=data.get("baseAccountId", ""),
             # Using 'external_id' but API returns 'externalId'
-            external_id=data.get("external_id", data.get("externalId", "")),
+            external_id=data.get("externalId", ""),
             arn=data.get("arn", "")
             # MISSING FIELDS that exist in actual API but not captured:
@@ -107,7 +107,7 @@
         """
         Parse pagination information from API response.

-        Uses baseline schema field names which differ from actual API response.
+        Uses baseline schema field names which differ from actual API response.
         """
         pageable = data.get("pageable", {})
         return PaginationInfo(
-            # Using 'page_number' but API returns 'pageNumber'
-            page_number=pageable.get("page_number", pageable.get("pageNumber", 0)),
+            # Using 'page_number' but API returns 'pageNumber'
+            page_number=pageable.get("pageNumber", 0),
             # Using 'page_size' but API returns 'pageSize'
-            page_size=pageable.get("page_size", pageable.get("pageSize", 0)),
+            page_size=pageable.get("pageSize", 0),
             # Using 'total_pages' but API returns 'totalPages'
-            total_pages=data.get("total_pages", data.get("totalPages", 0)),
+            total_pages=data.get("totalPages", 0),
             # Using 'total_elements' but API returns 'totalElements'
-            total_elements=data.get("total_elements", data.get("totalElements", 0)),
+            total_elements=data.get("totalElements", 0),
             # Using 'number_of_elements' but API returns 'numberOfElements'
-            number_of_elements=data.get("number_of_elements", data.get("numberOfElements", 0))
+            number_of_elements=data.get("numberOfElements", 0)
         )

     def fetch_connectors(self, page: int = 0, page_size: int = 50) -> ConnectorResponse:
@@ -133,7 +133,7 @@
             data = response.json()
             logger.info(f"Successfully fetched {len(data.get('content', []))} connectors")

-            return self._parse_response(data)
+            return self._parse_response(data)

         except requests.RequestException as e:
             logger.error(f"Failed to fetch connectors: {e}")
@@ -141,7 +141,7 @@
         except (KeyError, ValueError) as e:
             logger.error(f"Failed to parse response: {e}")
             raise ValueError(f"Invalid API response format: {e}")
-
+
     def _parse_response(self, data: Dict[str, Any]) -> ConnectorResponse:
         """Parse full API response into ConnectorResponse object."""
         content = data.get("content", [])
@@ -155,7 +155,7 @@
     def to_normalized_dict(self, connector: AWSConnector) -> Dict[str, Any]:
         """
         Convert connector to normalized dictionary format.
-
+
         This uses the BASELINE SCHEMA field names (snake_case) which differ
         from the actual API response (camelCase). CARE should detect this mismatch.
         """
@@ -163,14 +163,14 @@
             "name": connector.name,
             "connector_id": connector.connector_id,  # Should be 'connectorId'
             "description": connector.description,
-            "provider": connector.provider,
-            "status": connector.status,  # Should be 'state'
-            "total_assets": connector.total_assets,  # Should be 'totalAssets'
-            "last_synced_on": connector.last_synced_on,  # Should be 'lastSyncedOn'
-            "is_gov_cloud": connector.is_gov_cloud,  # Should be 'isGovCloud'
-            "is_china_region": connector.is_china_region,  # Should be 'isChinaRegion'
-            "aws_account_id": connector.aws_account_id,  # Should be 'awsAccountId'
-            "is_disabled": connector.is_disabled,  # Should be 'isDisabled'
-            "polling_frequency": {  # Should be 'pollingFrequency'
-                "hours": connector.polling_frequency.hours,
-                "minutes": connector.polling_frequency.minutes
-            },
-            "error": connector.error,
-            "base_account_id": connector.base_account_id,  # Should be 'baseAccountId'
-            "external_id": connector.external_id,  # Should be 'externalId'
-            "arn": connector.arn
-            # MISSING: nextSyncedOn, remediationEnabled, qualysTags, portalConnectorUuid, isPortalConnector
+            "provider": connector.provider,
+            "status": connector.status,  # Should be 'state'
+            "total_assets": connector.total_assets,  # Should be 'totalAssets'
+            "last_synced_on": connector.last_synced_on,  # Should be 'lastSyncedOn'
+            "is_gov_cloud": connector.is_gov_cloud,  # Should be 'isGovCloud'
+            "is_china_region": connector.is_china_region,  # Should be 'isChinaRegion'
+            "aws_account_id": connector.aws_account_id,  # Should be 'awsAccountId'
+            "is_disabled": connector.is_disabled,  # Should be 'isDisabled'
+            "polling_frequency": {  # Should be 'pollingFrequency'
+                "hours": connector.polling_frequency.hours,
+                "minutes": connector.polling_frequency.minutes
+            },
+            "error": connector.error,
+            "base_account_id": connector.base_account_id,  # Should be 'baseAccountId'
+            "external_id": connector.external_id,  # Should be 'externalId'
+            "arn": connector.arn
+            # MISSING: nextSyncedOn, remediationEnabled, qualysTags, portalConnectorUuid, isPortalConnector
         )