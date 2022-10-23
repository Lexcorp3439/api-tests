import io
import json
import time
from functools import lru_cache
from typing import Optional
from uuid import uuid4

import allure
from requests import PreparedRequest, Request, Response, Session

from src.config import config, consts


class HttpClient:

    def __init__(self, host: Optional[str] = None):
        if host:
            self.host = host
        else:
            self.host = config.URL

    def save_token_from_resp(self, response: Response):
        self.user_session().headers["Authorization"] = response.json()["token"]

    @lru_cache()
    def user_session(self) -> Session:
        session = Session()
        return session

    def send_request(
            self,
            request: Request,
            session: Session = None,
            message: Optional[str] = None
    ) -> Response:
        if session is None:
            session = self.user_session()

        request.url = self.host + request.url

        prepared_request = session.prepare_request(request)

        _message = f"Запрос {request.method.upper()} - {request.url}"
        if message is not None:
            _message = f"{_message} {message}"

        request_id = str(uuid4())
        with allure.step(_message):
            _curl_command = _request_to_curl(request=prepared_request)
            allure.attach(body=_curl_command, name="Curl command", attachment_type=consts.TEXT, )

            _request_message = request_message(prepared_request, request_id=request_id)
            allure.attach(body=_request_message, name="Request", attachment_type=consts.HTML, )

            response = session.send(prepared_request)

            _response_message = response_message(response, request_id=request_id)
            allure.attach(
                body=_response_message,
                name=f"Response ({str(int(time.time()))})",
                attachment_type=consts.HTML,
            )
            return response


def _text_body_to_json(text: str) -> str:
    try:
        text = json.loads(text)
        return json.dumps(text, indent=4, ensure_ascii=False)
    except Exception:
        return text


def _request_to_curl(request: PreparedRequest) -> str:
    headers = " \\\n  -H ".join([f'"{k}: {v}"' for k, v in request.headers.items()])
    body = request.body if hasattr(request, "body") else None

    if body and isinstance(body, bytes):
        try:
            body = body.decode()
        except UnicodeDecodeError:
            body = "@<use_file_from_allure>"

    method = request.method
    url = request.url
    return f"curl --compressed -i -X {method} \\\n  -H {headers} \\\n  -d '{body}' \\\n  '{url}'"


def request_message(request: PreparedRequest, request_id: str) -> str:
    if type(request.body) == bytes and request.body:
        body = request.body.decode("unicode-escape")
    elif type(request.body) == io.BufferedReader:
        body = "Binary File"
    else:
        body = _text_body_to_json(request.body)
    return _request_message_template.format(
        request_id=request_id,
        method=request.method,
        url=request.url,
        headers=request.headers,
        body=body,
    )


def response_message(response: Response, request_id: str) -> str:
    response_body = _text_body_to_json(response.text)
    return _response_message_template.format(
        request_id=request_id,
        status=response.status_code,
        reason=response.reason,
        elapsed=response.elapsed,
        headers=response.headers,
        body=response_body,
    )


_request_message_template = """
<strong>Request:</strong>
<ol style="list-style-type: none;">
<li><div style="word-wrap: break-word;"><strong>request-id:</strong> {request_id}</div></li>
<li><div style="word-wrap: break-word;"><strong>method:</strong> {method}</div></li>
<li><div style="word-wrap: break-word;"><strong>url:</strong> {url}</div></li>
<li><div style="word-wrap: break-word;"><strong>headers:</strong> {headers}</div></li>
<li><strong>body:</strong> <pre style="overflow-x: auto;white-space: pre-wrap;white-space: -moz-pre-wrap;
white-space: -pre-wrap;white-space: -o-pre-wrap;word-wrap: break-word;">{body}</pre></li>
</ol>
"""

_response_message_template = """
<strong>Response:</strong>
<ol style="list-style-type: none;">
<li><div style="word-wrap: break-word;"><strong>request-id:</strong> {request_id}</div></li>
<li><div style="word-wrap: break-word;"><strong>status-code:</strong> {status} {reason}</div></li>
<li><div style="word-wrap: break-word;"><strong>elapsed:</strong> {elapsed}</div></li>
<li><div style="word-wrap: break-word;"><strong>headers:</strong> {headers}</div></li>
<li><strong>body:</strong> <pre style="overflow-x: auto;white-space: pre-wrap;white-space: -moz-pre-wrap;
white-space: -pre-wrap;white-space: -o-pre-wrap;word-wrap: break-word;">{body}</pre></li>
</ol>
"""
