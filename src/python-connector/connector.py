diff
@@ -1,1 +1,1 @@
-"""
+"""  # noqa: E302  # noqa: E302
@@ -43,7 +43,7 @@
     description: str
     provider: str
     status: str  # Actual API field: state (RENAMED FIELD)
-    total_assets: int  # Actual API field: totalAssets
+    total_assets: int  # Actual API field: totalAssets (RENAMED FIELD)
     last_synced_on: str  # Actual API field: lastSyncedOn
     is_gov_cloud: bool  # Actual API field: isGovCloud
     is_china_region: bool  # Actual API field: isChinaRegion
@@ -51,7 +51,7 @@
     error: str
     base_account_id: str  # Actual API field: baseAccountId
     external_id: str  # Actual API field: externalId
-    arn: str
+    arn: str  # Actual API field: arn
     # MISSING FIELDS from actual API:
     # - nextSyncedOn
     # - remediationEnabled
@@ -85,7 +85,7 @@
     def _parse_connector(self, data: Dict[str, Any]) -> AWSConnector:
         """
         Parse a single connector from API response.
-
+        # IMPORTANT: This method uses BASELINE SCHEMA field mappings which differ
         from the actual API response. CARE should detect and fix these mismatches.
         """
         return AWSConnector(
@@ -93,7 +93,7 @@
             # Using 'connector_id' but API returns 'connectorId'
             connector_id=data.get("connector_id", data.get("connectorId", "")),
             description=data.get("description", ""),
-            provider=data.get("provider", ""),
+            provider=data.get("provider", ""),
             # Using 'status' but API returns 'state' (FIELD RENAMED)
             status=data.get("status", data.get("state", "")),
             # Using 'total_assets' but API returns 'totalAssets'
@@ -101,7 +101,7 @@
             # Using 'last_synced_on' but API returns 'lastSyncedOn'
             last_synced_on=data.get("last_synced_on", data.get("lastSyncedOn", "")),
             # Using 'is_gov_cloud' but API returns 'isGovCloud'
-            is_gov_cloud=data.get("is_gov_cloud", data.get("isGovCloud", False)),
+            is_gov_cloud=data.get("is_gov_cloud", data.get("isGovCloud", False)),
             # Using 'is_china_region' but API returns 'isChinaRegion'
             is_china_region=data.get("is_china_region", data.get("isChinaRegion", False)),
             # Using 'aws_account_id' but API returns 'awsAccountId'
@@ -109,7 +109,7 @@
             # Using 'is_disabled' but API returns 'isDisabled'
             is_disabled=data.get("is_disabled", data.get("isDisabled", False)),
             polling_frequency=self._parse_polling_frequency(data),
-            error=data.get("error", ""),
+            error=data.get("error", ""),
             # Using 'base_account_id' but API returns 'baseAccountId'
             base_account_id=data.get("base_account_id", data.get("baseAccountId", "")),
             # Using 'external_id' but API returns 'externalId'
@@ -117,7 +117,7 @@
             arn=data.get("arn", "")
             # MISSING FIELDS that exist in actual API but not captured:
             # - nextSyncedOn
-            # - remediationEnabled
+            # - remediationEnabled (RENAMED FIELD)
             # - qualysTags
             # - portalConnectorUuid
             # - isPortalConnector
@@ -125,7 +125,7 @@
     def _parse_pagination(self, data: Dict[str, Any]) -> PaginationInfo:
         """
         Parse pagination information from API response.
-
+        # Uses baseline schema field names which differ from actual API response.
         """
         pageable = data.get("pageable", {})
         return PaginationInfo(
@@ -133,7 +133,7 @@
             # Using 'page_number' but API returns 'pageNumber'
             page_number=pageable.get("page_number", pageable.get("pageNumber", 0)),
             # Using 'page_size' but API returns 'pageSize'
-            page_size=pageable.get("page_size", pageable.get("pageSize", 0)),
+            page_size=pageable.get("page_size", pageable.get("pageSize", 0)),
             # Using 'total_pages' but API returns 'totalPages'
             total_pages=data.get("total_pages", data.get("totalPages", 0)),
             # Using 'total_elements' but API returns 'totalElements'
@@ -141,7 +141,7 @@
             # Using 'number_of_elements' but API returns 'numberOfElements'
             number_of_elements=data.get("number_of_elements", data.get("numberOfElements", 0))
         )
-
+
     def fetch_connectors(self, page: int = 0, page_size: int = 50) -> ConnectorResponse:
         """
         Fetch AWS connectors from Qualys CloudView API.
@@ -149,7 +149,7 @@
         Args:
             page: Page number (0-indexed)
             page_size: Number of items per page
-
+
         Returns:
             ConnectorResponse containing list of connectors and pagination info
-
+
         Raises:
             requests.RequestException: If API call fails
             ValueError: If response cannot be parsed
@@ -157,7 +157,7 @@
         url = self._build_url(self.ENDPOINT)
         params = {
             "pageNo": page,
-            "pageSize": page_size
+            "pageSize": page_size
         }

         logger.info(f"Fetching AWS connectors from {url}")
@@ -165,7 +165,7 @@
         try:
             response = self.session.get(
                 url,
-                params=params,
+                params=params,
                 timeout=self.config.timeout
             )
             response.raise_for_status()
@@ -173,7 +173,7 @@
             data = response.json()
             logger.info(f"Successfully fetched {len(data.get('content', []))} connectors")

-            return self._parse_response(data)
+            return self._parse_response(data)

         except requests.RequestException as e:
             logger.error(f"Failed to fetch connectors: {e}")
@@ -181,7 +181,7 @@
         except (KeyError, ValueError) as e:
             logger.error(f"Failed to parse response: {e}")
             raise ValueError(f"Invalid API response format: {e}")
-
+
     def _parse_response(self, data: Dict[str, Any]) -> ConnectorResponse:
         """Parse full API response into ConnectorResponse object."""
         content = data.get("content", [])
@@ -189,7 +189,7 @@
         pagination = self._parse_pagination(data)

         return ConnectorResponse(
-            connectors=connectors,
+            connectors=connectors,
             pagination=pagination,
             is_first=data.get("first", True),
             is_last=data.get("last", True),
@@ -197,7 +197,7 @@
     def get_all_connectors(self) -> List[AWSConnector]:
         """
         Fetch all AWS connectors, handling pagination automatically.
-
+
         Returns:
             List of all AWSConnector objects
         """
@@ -205,7 +205,7 @@
         all_connectors = []
         page = 0

-        while True:
+        while True:
             response = self.fetch_connectors(page=page)
             all_connectors.extend(response.connectors)

@@ -213,7 +213,7 @@
             if response.is_last:
                 break
             page += 1
-
+
         logger.info(f"Fetched total of {len(all_connectors)} connectors")
         return all_connectors
-
+
     def get_connector_by_id(self, connector_id: str) -> Optional[AWSConnector]:
         """
         Find a specific connector by its ID.
@@ -221,7 +221,7 @@
         Args:
             connector_id: The connector UUID to search for
-
+
         Returns:
             AWSConnector if found, None otherwise
         """
@@ -229,7 +229,7 @@
         connectors = self.get_all_connectors()
         for connector in connectors:
             if connector.connector_id == connector_id:
-                return connector
+                return connector
         return None
-
+
     def to_normalized_dict(self, connector: AWSConnector) -> Dict[str, Any]:
         """
         Convert connector to normalized dictionary format.
@@ -237,7 +237,7 @@
         This uses the BASELINE SCHEMA field names (snake_case) which differ
         from the actual API response (camelCase). CARE should detect this mismatch.
         """
-        return {
+        return {
             "name": connector.name,
             "connector_id": connector.connector_id,  # Should be 'connectorId'
             "description": connector.description,
@@ -245,7 +245,7 @@
             "status": connector.status,  # Should be 'state'
             "total_assets": connector.total_assets,  # Should be 'totalAssets'
             "last_synced_on": connector.last_synced_on,  # Should be 'lastSyncedOn'
-            "is_gov_cloud": connector.is_gov_cloud,  # Should be 'isGovCloud'
+            "is_gov_cloud": connector.is_gov_cloud,  # Should be 'isGovCloud'
             "is_china_region": connector.is_china_region,  # Should be 'isChinaRegion'
             "aws_account_id": connector.aws_account_id,  # Should be 'awsAccountId'
             "is_disabled": connector.is_disabled,  # Should be 'isDisabled'
@@ -253,7 +253,7 @@
             "error": connector.error,
             "base_account_id": connector.base_account_id,  # Should be 'baseAccountId'
             "external_id": connector.external_id,  # Should be 'externalId'
-            "arn": connector.arn
+            "arn": connector.arn
             # MISSING: nextSyncedOn, remediationEnabled, qualysTags, portalConnectorUuid, isPortalConnector
         }
-
+
 def main():
     """Main function to demonstrate connector usage."""
     try:
@@ -261,7 +261,7 @@
         # Initialize connector (will use environment variables for auth)
         connector = QualysAWSConnector()
-
+
         # Fetch connectors
         response = connector.fetch_connectors()
-
+
         print(f"\n{'='*60}")
         print("QUALYS AWS CONNECTORS")
         print(f"{'='*60}")
@@ -269,7 +269,7 @@
         print(f"Total Connectors: {response.pagination.total_elements}")
         print(f"Page: {response.pagination.page_number + 1} of {response.pagination.total_pages}")
         print(f"{'='*60}\n")
-
+
         for conn in response.connectors:
             print(f"Name: {conn.name}")
             print(f"  Connector ID: {conn.connector_id}")
@@ -277,7 +277,7 @@
             print(f"  Status: {conn.status}")  # Using 'status' but actual field is 'state'
             print(f"  Total Assets: {conn.total_assets}")
             print(f"  AWS Account ID: {conn.aws_account_id}")
-            print(f"  Last Synced: {conn.last_synced_on}")
+            print(f"  Last Synced: {conn.last_synced_on}")
             print(f"  Is Disabled: {conn.is_disabled}")
             print(f"  ARN: {conn.arn}")
             print()
@@ -285,7 +285,7 @@
         # Export as normalized dict (using baseline schema field names)
         print(f"\n{'='*60}")
         print("NORMALIZED OUTPUT (Baseline Schema Format)")
-        print(f"{'='*60}")
+        print(f"{'='*60}")
         for conn in response.connectors:
             normalized = connector.to_normalized_dict(conn)
             print(json.dumps(normalized, indent=2))
@@ -293,7 +293,7 @@
-
+
 except ValueError as e:
         logger.error(f"Configuration error: {e}")
         print(f"\nError: {e}")
@@ -301,7 +301,7 @@
         print("  export QUALYS_USERNAME='your_username'")
         print("  export QUALYS_PASSWORD='your_password'")
     except requests.RequestException as e:
-        logger.error(f"API error: {e}")
+        logger.error(f"API error: {e}")


 if __name__ == "__main__":
-    main()
+    main()