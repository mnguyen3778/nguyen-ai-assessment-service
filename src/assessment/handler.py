from dataclasses import replace
import json
from typing import Any
from uuid import uuid4

from assessment.scoring import score_assessment
from assessment.validation import validate_assessment_request


ALLOWED_CORS_ORIGINS = frozenset(
    {
        "http://localhost:3000",
        "https://nguyen-ai.com",
    }
)


def handle_assessment(event: dict[str, Any]) -> dict[str, Any]:
    request_id = str(uuid4())
    validation_result = validate_assessment_request(event.get("body"))

    if not validation_result.is_valid:
        return _json_response(
            400,
            {
                "requestId": request_id,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Assessment request is invalid.",
                    "details": [
                        error.to_dict()
                        for error in validation_result.errors
                    ],
                },
                "modelInvoked": False,
                "persisted": False,
            },
            event,
        )

    assessment_response = replace(
        score_assessment(validation_result.request),
        requestId=request_id,
    )
    return _json_response(200, assessment_response.to_dict(), event)


def _json_response(
    status_code: int,
    body: dict[str, Any],
    event: dict[str, Any],
) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": _response_headers(event),
        "body": json.dumps(body),
    }


def _response_headers(event: dict[str, Any]) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Vary": "Origin",
        "Access-Control-Allow-Headers": "Authorization,Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST",
    }
    origin = _request_origin(event)
    if origin in ALLOWED_CORS_ORIGINS:
        headers["Access-Control-Allow-Origin"] = origin

    return headers


def _request_origin(event: dict[str, Any]) -> str | None:
    request_headers = event.get("headers")
    if not isinstance(request_headers, dict):
        return None

    for name, value in request_headers.items():
        if isinstance(name, str) and name.lower() == "origin":
            return value if isinstance(value, str) else None

    return None
