from typing import Dict
import copy

from flask_restx import fields  # type:ignore
import flask_restx  # type:ignore

from foodbank_southlondon.api import models
from foodbank_southlondon.api.requests import models as requests_models
from foodbank_southlondon.api.events import models as events_models
from foodbank_southlondon.bff import rest


_pagination = rest.model("ResultsPage", models.pagination_fields)


def _clone_field_without_attribute(field: fields.Raw) -> fields.Raw:
    field_copy = copy.copy(field)
    field_copy.attribute = None
    return field_copy


def _clone_fields_without_attribute(model: flask_restx.Model) -> Dict:
    return {k: _clone_field_without_attribute(v) for k, v in model.items()}


_event = rest.model("EventSummary", {
    "event_timestamp": events_models.event["event_timestamp"],
    "event_name": events_models.event["event_name"],
    "event_date": events_models.event["event_date"]
})

_request = rest.model("ClientRequest", _clone_fields_without_attribute(requests_models.request))

_similar_request_summary = rest.model("SimilarClientRequestSummary", {
    "request_id": requests_models.request["request_id"],
    "timestamp": _clone_field_without_attribute(requests_models.request["timestamp"]),
    "client_full_name": _clone_field_without_attribute(requests_models.request["client_full_name"]),
    "postcode": _clone_field_without_attribute(requests_models.request["postcode"])
})

_status = rest.inherit("Status", _event, {
    "request_id": requests_models.request["request_id"],
    "client_full_name": _clone_field_without_attribute(requests_models.request["client_full_name"]),
    "reference_number": _clone_field_without_attribute(requests_models.request["reference_number"]),
    "postcode": _clone_field_without_attribute(requests_models.request["postcode"]),
    "delivery_date": _clone_field_without_attribute(requests_models.request["delivery_date"])
})

action = rest.model("Action", {
    "request_ids": fields.List(requests_models.request["request_id"]),
    "event_names": fields.List(events_models.event["event_name"]),
    "event_date": events_models.event["event_date"]
})

details = rest.model("ClientRequestDetails", {
    "request": fields.Nested(_request),
    "events": fields.List(fields.Nested(_event)),
    "similar_request_ids": fields.List(fields.Nested(_similar_request_summary))
})

page_of_status = rest.inherit("StatusPage", _pagination, {
    "items": fields.List(fields.Nested(_status))
})