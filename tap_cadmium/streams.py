"""Stream type classes for tap-cadmium."""

from __future__ import annotations

import typing as t
import requests
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_cadmium.client import cadmiumStream


class SubmissionsStream(cadmiumStream):
    """Stream for Cadmium Submissions API."""
    
    name = "submissions"
    path = "webservices/api.asp"
    primary_keys = ["SubmissionID"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("SubmissionID", th.StringType),
        th.Property("SubmitterID", th.StringType),
        th.Property("SubmissionStatus", th.StringType),
        th.Property("SubmissionDateAdded", th.DateTimeType),
        th.Property("SubmissionDateCompleted", th.DateTimeType),
        th.Property("SubmissionTypeID", th.StringType),
        th.Property("SubmissionCategory", th.StringType),
    ).to_dict()

    def get_url_params(
        self,
        context: th.Optional[dict],
        next_page_token: th.Optional[th.Any]
    ) -> th.Dict[str, th.Any]:
        params = super().get_url_params(context, next_page_token)
        params.update({
            "Method": "getSubmissions",
            "eID": self.config["eidsub"],
            "page": next_page_token or 1
        })
        return params
    
class AuthorsStream(cadmiumStream):
    """Stream for Cadmium Submissions API."""
    
    name = "authors"
    path = "webservices/api.asp"
    primary_keys = ["AuthorID"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("AuthorID", th.StringType),
        th.Property("AuthorKey", th.StringType),
        th.Property("AuthorFirstName", th.StringType),
        th.Property("AuthorLastName", th.StringType),
        th.Property("AuthorEmail", th.StringType),
        th.Property("AuthorState", th.StringType),
        th.Property("AuthorCountry", th.StringType),
        th.Property("AuthorOrganization", th.StringType),   
    ).to_dict()

    def get_url_params(
        self,
        context: th.Optional[dict],
        next_page_token: th.Optional[th.Any]
    ) -> th.Dict[str, th.Any]:
        params = super().get_url_params(context, next_page_token)
        params.update({
            "Method": "getAuthors",
            "eID": self.config["eidaut"],
            "page": next_page_token or 1
        })
        return params
    
class SubmittersStream(cadmiumStream):
    """Stream for Cadmium Submissions API."""
    
    name = "submitters"
    path = "webservices/api.asp"
    primary_keys = ["SubmitterID"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("SubmitterID", th.StringType),
        th.Property("SubmitterFirstName", th.StringType),
        th.Property("SubmitterEmail", th.StringType),
        th.Property("SubmitterMemberID", th.StringType),
        th.Property("SubmitterChairRole", th.StringType),
        th.Property("SubmitterIDExternalSystem", th.StringType),  
    ).to_dict()

    def get_url_params(
        self,
        context: th.Optional[dict],
        next_page_token: th.Optional[th.Any]
    ) -> th.Dict[str, th.Any]:
        params = super().get_url_params(context, next_page_token)
        params.update({
            "Method": "getSubmitters",
            "eID": self.config["eidaut"],
            "page": next_page_token or 1
        })
        return params
