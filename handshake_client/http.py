import json
import requests
from typing import Union, List, Dict, Any
from handshake_client.constant import TIMEOUT


class HttpClient:
    def __init__(self, endpoint: str, timeout: int = TIMEOUT):
        assert type(endpoint) == str
        assert type(timeout) == int
        self.endpoint = endpoint
        self.timeout = timeout

    def get(self, method: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert method == str
        r = requests.get(self.endpoint + "/" + method, timeout=self.timeout)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return json.loads(e.response.content)
        return r.json()

    def post(self, method: str, params: Dict[str, Any]) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert method == str
        assert params == dict
        headers = {"Content-Type": "application/json"}
        r = requests.post(self.endpoint + "/" + method, data=json.dumps(params), headers=headers, timeout=self.timeout)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return json.loads(e.response.content)
        return r.json()
