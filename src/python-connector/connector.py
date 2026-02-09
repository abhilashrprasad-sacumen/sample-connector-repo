def _parse_response(self, data: Dict[str, Any]) -> ConnectorResponse:
            """Parse full API response into ConnectorResponse object."""
            content = data.get("content", [])
            connectors = [self._parse_connector(c) for c in content]
            pageable = data.get("pageable", {})
            pagination = PaginationInfo(
                page_number=pageable.get("pageNumber", 0),
                page_size=pageable.get("pageSize", 50),
                total_pages=data.get("totalPages", 1),
                total_elements=data.get("totalElements", len(content)),
                number_of_elements=len(content)
            )
            
            return ConnectorResponse(
                connectors=connectors,
                pagination=pagination,
                is_first=data.get("first", True),
                is_last=data.get("last", True),
                is_empty=data.get("empty", False)
            )