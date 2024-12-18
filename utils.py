import requests
from datetime import datetime
import json


def make_request(session_state):
    headers = {}
    for i in range(len(session_state["header_keys"])):
        if (
            session_state["header_keys"][i] != ""
            and session_state["header_values"][i] != ""
        ):
            headers[session_state["header_keys"][i]] = session_state["header_values"][i]

    session_state["headers"] = headers
    session_state["request_time"] = datetime.now()

    response = requests.request(
        session_state["method"],
        session_state["url"],
        headers=headers,
        data=session_state["request_body"],
    )

    session_state["response_time"] = datetime.now()
    session_state["response_code"] = response.status_code
    session_state["response_headers"] = dict(response.headers)
    session_state["response_body"] = response.text

    return session_state


def check_value(headers):
    quantity = len(headers)
    if quantity == 0:
        quantity = 1
    return quantity


def format_download_json(session_state):
    session_state_copy = {key: value for key, value in session_state.items()}

    session_state_copy["test_duration"] = str(
        session_state_copy["response_time"] - session_state_copy["request_time"]
    )
    session_state_copy["response_time"] = session_state_copy[
        "response_time"
    ].isoformat()
    session_state_copy["request_time"] = session_state_copy["request_time"].isoformat()

    if "header_keys" in session_state_copy:
        del session_state_copy["header_keys"]
    if "header_values" in session_state_copy:
        del session_state_copy["header_values"]

    json_bytes = json.dumps(session_state_copy).encode("utf-8")
    return json_bytes
