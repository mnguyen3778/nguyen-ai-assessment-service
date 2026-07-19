from typing import Any

from assessment.handler import handle_assessment


def lambda_handler(
    event: dict[str, Any],
    context: Any,
) -> dict[str, Any]:
    return handle_assessment(event)
