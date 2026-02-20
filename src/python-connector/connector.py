ANALYSIS:
The code needs to be updated to include the new fields introduced in the API response. Specifically, the `ConnectorResponse` class and the `_parse_response` method need to be modified to handle the new `content`, `first`, `last`, and `empty` fields.

ROOT_CAUSE:
The API schema mismatch is causing the breakage because the code does not account for the new optional fields introduced in the response.

PATCH: