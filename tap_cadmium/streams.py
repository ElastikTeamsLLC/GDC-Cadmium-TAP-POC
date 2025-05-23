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
    """Stream for Cadmium Authors API."""
    
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
    """Stream for Cadmium Submitters API."""
    
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

class AbstractsStream(cadmiumStream):
    """Stream for Cadmium Abstracts API."""
    
    name = "abstracts"
    path = "webservices/api.asp"
    primary_keys = ["AbstractID"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("AbstractID", th.StringType),
        th.Property("SubmissionID", th.StringType),
        th.Property("SubmitterID", th.StringType),
        th.Property("AbstractTopic", th.StringType),
        th.Property("AbstractText0", th.StringType),
        th.Property("AbstractTargetAudience", th.StringType),  
    ).to_dict()

    def get_url_params(
        self,
        context: th.Optional[dict],
        next_page_token: th.Optional[th.Any]
    ) -> th.Dict[str, th.Any]:
        params = super().get_url_params(context, next_page_token)
        params.update({
            "Method": "getAbstracts",
            "eID": self.config["eidabs"],
            "page": next_page_token or 1
        })
        return params
    
    
class ReviewsStream(cadmiumStream):
    """Stream for Cadmium Reviews API."""
    
    name = "reviews"
    path = "webservices/api.asp"
    primary_keys = ["ReviewID"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("ReviewID", th.StringType),
        th.Property("ReviewDateAdded", th.StringType),
        th.Property("ReviewDateEdited", th.StringType),
        th.Property("ReviewSubmissionID", th.StringType),
        th.Property("ReviewReviewerID", th.StringType),
    ).to_dict()

    def get_url_params(
        self,
        context: th.Optional[dict],
        next_page_token: th.Optional[th.Any]
    ) -> th.Dict[str, th.Any]:
        params = super().get_url_params(context, next_page_token)
        params.update({
            "Method": "getReviews",
            "eID": self.config["eidaut"],
            "page": next_page_token or 1
        })
        return params
    
class PresentersStream(cadmiumStream):
    """Stream for Cadmium Presenters API."""
    name = "presenters"
    path = "webservices/HarvesterJsonAPI.asp"
    replication_key = None
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("PresenterID", th.StringType),
        th.Property("PresenterDateAdded", th.StringType),
        th.Property("PresenterDateEdited", th.StringType),
        th.Property("PresenterFirstName", th.StringType),
        th.Property("PresenterLastName", th.StringType),
        th.Property("PresenterPosition", th.StringType),
        th.Property("PresenterOrganization", th.StringType),
        th.Property("PresenterEmail", th.StringType),
        th.Property("PresenterCountry", th.StringType),
    ).to_dict()
    
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["pres_url"]
    
    def get_url_params(
        self,
        context: th.Optional[dict],
        next_page_token : th.Optional[th.Any]
    ) -> th.Dict[str, th.Any]:
        params = super().get_url_params(context, next_page_token)
        params.update({
            "Method": "getPresenters",
            "eID": self.config["eidpre"]
        })
        return params
    
    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: t.Optional[t.Any]
    ) -> t.Optional[t.Any]:
        # No pagination required for this endpoint
        return None

    
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        return response.json()


class PresentationsStream(cadmiumStream):
    """Stream for Cadmium Presentations API."""
    name = "presentations"
    path = "webservices/HarvesterJsonAPI.asp"
    replication_key = None
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("EventName", th.StringType),
        th.Property("EventID", th.StringType),
        th.Property("EventKey", th.StringType),
        th.Property("PresentationID", th.StringType),
        th.Property("PresentationStatus", th.StringType),
        th.Property("PresentationDateAdded", th.StringType),
        th.Property("PresentationDateEdited", th.StringType),
        th.Property("PresentationDate", th.StringType),
        th.Property("SessionStartTime", th.StringType),
        th.Property("SessionEndTime", th.StringType),
        th.Property("PresentationTitle", th.StringType),
        th.Property("AbstractText", th.StringType),
    ).to_dict()
    
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["pres_url"]
    
    def get_url_params(
        self,
        context: th.Optional[dict],
        next_page_token : th.Optional[th.Any]
    ) -> th.Dict[str, th.Any]:
        params = super().get_url_params(context, next_page_token)
        params.update({
            "Method": "getPresentations",
            "eID": self.config["eidaut"]
        })
        return params
    
    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: t.Optional[t.Any]
    ) -> t.Optional[t.Any]:
        # No pagination required for this endpoint
        return None

    
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        return response.json()