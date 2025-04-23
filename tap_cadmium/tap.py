"""cadmium tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_cadmium import streams


class Tapcadmium(Tap):
    """cadmium tap class."""

    name = "tap-cadmium"

    config_jsonschema = th.PropertiesList(
        th.Property("api_key", th.StringType, required=True),
        th.Property("api_url", th.StringType, required=True),
    ).to_dict()

    def discover_streams(self) -> list[streams.cadmiumStream]:
        """Return a list of discovered streams."""
        return [
            # streams.SubmissionsStream(self),
            # streams.AuthorsStream(self),
            # streams.SubmittersStream(self),
            # streams.AbstractsStream(self),
            # streams.ReviewsStream(self),
            streams.PresentersStream(self),
        ]


if __name__ == "__main__":
    Tapcadmium.cli()