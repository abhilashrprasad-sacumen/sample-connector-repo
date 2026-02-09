def _parse_response(self, data: Dict[str, Any]) -> ConnectorResponse:
            """Parse full API response into ConnectorResponse object."""
            content = data.get("pageable", {}).get("content", [])
            connectors = [self._parse_connector(c) for c in content]
            pagination = self._parse_pagination(data)
            
            return ConnectorResponse(
                connectors=connectors,
                pagination=pagination,
                is_first=data.get("first", True),
                is_last=data.get("last", True),
                is_empty=data.get("empty", False)
            )