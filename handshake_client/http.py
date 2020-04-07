import json
from requests import get, post
from requests.exceptions import ConnectionError, HTTPError
from typing import cast, Union, List, Dict, Any
from handshake_client.constant import TIMEOUT


class Request:
    def __init__(self, endpoint: str, timeout: int = TIMEOUT):
        assert type(endpoint) == str
        assert type(timeout) == int
        self.endpoint = endpoint
        self.timeout = timeout

    def get(self, method: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert type(method) == str
        try:
            r = get(self.endpoint + "/" + method, timeout=self.timeout)
            r.raise_for_status()
        except (ConnectionError, HTTPError) as e:
            # return handshake Errors format
            return {"error": {"message": str(e)}}
        return r.json()

    def post(self, method: str, params: Dict[str, Any]) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert type(method) == str
        assert type(params) == dict
        headers = {"Content-Type": "application/json"}
        try:
            r = post(self.endpoint + "/" + method, data=json.dumps(params), headers=headers, timeout=self.timeout)
            r.raise_for_status()
        except (ConnectionError, HTTPError) as e:
            # return handshake Errors format
            return {"error": {"message": str(e)}}
        return r.json()


class HttpClient:
    def __init__(self, api_key: str, host: str, port: str, user: str = "x", ssl: bool = False, timeout: int = TIMEOUT):
        assert type(api_key) == str
        assert type(host) == str
        assert type(port) == str
        assert type(user) == str
        assert type(ssl) == bool
        assert type(timeout) == int
        schema: str = "http"
        if ssl is True:
            schema = "https"
        endpoint = f"{schema}://{user}:{api_key}@{host}:{port}"
        self.request = Request(endpoint, timeout)

    def get_info(self) -> Dict[str, Any]:
        r = self.request.get("")
        result = cast(Dict[str, Any], r)
        return result

    def get_mempool(self) -> List[str]:
        r = self.request.get("mempool")
        result = cast(List[str], r)
        return result

    def get_mempool_invalid(self) -> Dict[str, Any]:
        r = self.request.get("mempool/invalid")
        result = cast(Dict[str, Any], r)
        return result

    def get_mempool_invalid_by_hash(self, hash: str) -> Dict[str, bool]:
        assert type(hash) == str
        r = self.request.get(f"mempool/invalid/{hash}")
        result = cast(Dict[str, bool], r)
        return result

    def get_block_by_hash(self, hash: str) -> Dict[str, Any]:
        assert type(hash) == str
        r = self.request.get(f"block/{hash}")
        result = cast(Dict[str, Any], r)
        return result

    def get_block_by_height(self, height: str) -> Dict[str, Any]:
        assert type(height) == str
        r = self.request.get(f"block/{height}")
        result = cast(Dict[str, Any], r)
        return result

    def broadcast_tx(self, tx_hex: str) -> Dict[str, bool]:
        assert type(tx_hex) == str
        params = {"tx": tx_hex}
        r = self.request.post("broadcast", params)
        result = cast(Dict[str, bool], r)
        return result

    def broadcast_claim(self, claim: str) -> Dict[str, bool]:
        assert type(claim) == str
        params = {"claim": claim}
        r = self.request.post("claim", params)
        result = cast(Dict[str, bool], r)
        return result

    def estimate_fee(self, blocks: int) -> Dict[str, int]:
        assert type(blocks) == int
        r = self.request.get(f"fee?blocks={blocks}")
        result = cast(Dict[str, int], r)
        return result

    def reset(self, height: int) -> Dict[str, bool]:
        assert type(height) == int
        params = {"height": height}
        r = self.request.post("reset", params)
        result = cast(Dict[str, bool], r)
        return result

    def get_coin_by_hash_and_index(self, hash: str, index: str) -> Dict[str, Any]:
        assert type(hash) == str
        assert type(index) == str
        r = self.request.get(f"coin/{hash}/{index}")
        result = cast(Dict[str, Any], r)
        return result

    def get_coin_by_address(self, address: str) -> Dict[str, Any]:
        assert type(address) == str
        r = self.request.get(f"coin/address/{address}")
        result = cast(Dict[str, Any], r)
        return result

    def get_coin_by_addresses(self, addresses: List[str]) -> Dict[str, Any]:
        assert type(addresses) == list
        params = {"address": addresses}
        r = self.request.post(f"coin/address", params)
        result = cast(Dict[str, Any], r)
        return result

    def get_tx_by_hash(self, tx_hash: str) -> Dict[str, Any]:
        assert type(tx_hash) == str
        r = self.request.get(f"tx/{tx_hash}")
        result = cast(Dict[str, Any], r)
        return result

    def get_tx_by_address(self, address: str) -> Dict[str, Any]:
        assert type(address) == str
        r = self.request.get(f"tx/address/{address}")
        result = cast(Dict[str, Any], r)
        return result

    def get_tx_by_addresses(self, addresses: List[str]) -> Dict[str, Any]:
        assert type(addresses) == list
        params = {"address": addresses}
        r = self.request.post(f"tx/address", params)
        result = cast(Dict[str, Any], r)
        return result
