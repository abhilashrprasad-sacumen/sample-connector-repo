diff
--- a/qualys_aws_connector.py
+++ b/qualys_aws_connector.py
@@ -100,7 +100,7 @@
         return AWSConnector(
             name=data.get("name", ""),
             # Using 'connector_id' but API returns 'connectorId'
-            connector_id=data.get("connector_id", data.get("connectorId", "")),
+            connector_id=data.get("connectorId", data.get("connectorId", "")),
             description=data.get("description", ""),
             provider=data.get("provider", ""),
             # Using 'status' but API returns 'state' (FIELD RENAMED)
@@ -110,7 +110,7 @@
             # Using 'total_assets' but API returns 'totalAssets'
-            total_assets=data.get("total_assets", data.get("totalAssets", 0)),
+            total_assets=data.get("totalAssets", data.get("totalAssets", 0)),
             # Using 'last_synced_on' but API returns 'lastSyncedOn'
-            last_synced_on=data.get("last_synced_on", data.get("lastSyncedOn", "")),
+            last_synced_on=data.get("lastSyncedOn", data.get("lastSyncedOn", "")),
             # Using 'is_gov_cloud' but API returns 'isGovCloud'
-            is_gov_cloud=data.get("is_gov_cloud", data.get("isGovCloud", False)),
+            is_gov_cloud=data.get("isGovCloud", data.get("isGovCloud", False)),
             # Using 'is_china_region' but API returns 'isChinaRegion'
-            is_china_region=data.get("is_china_region", data.get("isChinaRegion", False)),
+            is_china_region=data.get("isChinaRegion", data.get("isChinaRegion", False)),
             # Using 'aws_account_id' but API returns 'awsAccountId'
-            aws_account_id=data.get("aws_account_id", data.get("awsAccountId", "")),
+            aws_account_id=data.get("awsAccountId", data.get("awsAccountId", "")),
             # Using 'is_disabled' but API returns 'isDisabled'
-            is_disabled=data.get("is_disabled", data.get("isDisabled", False)),
+            is_disabled=data.get("isDisabled", data.get("isDisabled", False)),
             polling_frequency=self._parse_polling_frequency(data),
             error=data.get("error", ""),
             # Using 'base_account_id' but API returns 'baseAccountId'
-            base_account_id=data.get("base_account_id", data.get("baseAccountId", "")),
+            base_account_id=data.get("baseAccountId", data.get("baseAccountId", "")),
             # Using 'external_id' but API returns 'externalId'
-            external_id=data.get("external_id", data.get("externalId", "")),
+            external_id=data.get("externalId", data.get("externalId", "")),
             arn=data.get("arn", "")
             # MISSING FIELDS that exist in actual API but not captured:
             # - nextSyncedOn
             # - remediationEnabled
             # - qualysTags
             # - portalConnectorUuid
             # - isPortalConnector
@@ -122,7 +122,7 @@
         page_number=pageable.get("page_number", pageable.get("pageNumber", 0)),
         # Using 'page_size' but API returns 'pageSize'
         page_size=pageable.get("page_size", pageable.get("pageSize", 0)),
-        # Using 'total_pages' but API returns 'totalPages'
+        # Using 'total_pages' but API returns 'totalPages'
         total_pages=data.get("total_pages", data.get("totalPages", 0)),
         # Using 'total_elements' but API returns 'totalElements'
         total_elements=data.get("total_elements", data.get("totalElements", 0)),
@@ -130,7 +130,7 @@
         number_of_elements=data.get("number_of_elements", data.get("numberOfElements", 0))
     )
 
-    # Using 'connector_id' but API returns 'connectorId'
-    connector_id=data.get("connector_id", data.get("connectorId", "")),
-    # Using 'total_assets' but API returns 'totalAssets'
-    total_assets=data.get("total_assets", data.get("totalAssets", 0)),
-    # Using 'remediation_enabled' but API returns 'remediationEnabled'
-    remediation_enabled=data.get("remediation_enabled", data.get("remediationEnabled", False)),
+    # Using 'connector_id' but API returns 'connectorId'
+    connector_id=data.get("connectorId", data.get("connectorId", "")),
+    # Using 'total_assets' but API returns 'totalAssets'
+    total_assets=data.get("totalAssets", data.get("totalAssets", 0)),
+    # Using 'remediation_enabled' but API returns 'remediationEnabled'
+    remediation_enabled=data.get("remediationEnabled", data.get("remediationEnabled", False)),
 
     return ConnectorResponse(
         connectors=connectors,
         pagination=pagination,
         is_first=data.get("first", True),
         is_last=data.get("last", True),
         is_empty=data.get("empty", False)
     )