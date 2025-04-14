"""REST client handling, including cadmiumStream base class."""

from __future__ import annotations

import typing as t
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class cadmiumStream(RESTStream):
    """cadmium stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    def request_headers(self, context: dict | None, next_page_token: t.Any) -> dict:
        """Return the headers for API requests."""
        return {
            "Accept": "application/json"
        }

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        params["APIKey"] = self.config["api_key"]
        
        if next_page_token:
            params["page"] = next_page_token
            
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
            
        return params
    
    #The method below is used to get the next page token from the response.
    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: t.Optional[t.Any]
    ) -> t.Optional[int]:
        data = response.json()
        current_page = data["metadata"]["page"]
        total_pages = data["metadata"]["pages"]
        if current_page < total_pages:
            return current_page + 1
        return None
    
    #The method below is used to parse the response from the API.
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        data = response.json()
        # current_page = data["metadata"]["page"]
        # total_pages = data["metadata"]["pages"]
        
        # print(f"\nProcessing page {current_page} of {total_pages}")
        # print(f"Found {len(data.get('results', []))} records on this page\n")
        
        return data.get("results", [])
    
