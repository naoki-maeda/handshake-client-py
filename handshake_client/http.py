import json
from requests import get, post, put
from requests.exceptions import ConnectionError, HTTPError
from typing import cast, Optional, Union, List, Dict, Any
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

    def post(
        self, method: str, params: Dict[str, Any]
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert type(method) == str
        assert type(params) == dict
        headers = {"Content-Type": "application/json"}
        try:
            r = post(
                self.endpoint + "/" + method,
                data=json.dumps(params),
                headers=headers,
                timeout=self.timeout,
            )
            r.raise_for_status()
        except (ConnectionError, HTTPError) as e:
            # return handshake Errors format
            return {"error": {"message": str(e)}}
        return r.json()

    def put(
        self, method: str, params: Dict[str, Any]
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert type(method) == str
        assert type(params) == dict
        try:
            r = put(
                self.endpoint + "/" + method,
                data=json.dumps(params),
                timeout=self.timeout,
            )
            r.raise_for_status()
        except (ConnectionError, HTTPError) as e:
            # return handshake Errors format
            return {"error": {"message": str(e)}}
        return r.json()


class HttpClient:
    def __init__(
        self,
        api_key: str,
        host: str,
        port: str,
        user: str = "x",
        ssl: bool = False,
        timeout: int = TIMEOUT,
    ):
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


class WalletHttpClient:
    def __init__(
        self,
        api_key: str,
        host: str,
        port: str,
        user: str = "x",
        ssl: bool = False,
        timeout: int = TIMEOUT,
    ):
        assert type(api_key) == str
        assert type(host) == str
        assert type(port) == str
        assert type(user) == str
        assert type(ssl) == bool
        assert type(timeout) == int
        schema: str = "http"
        if ssl is True:
            schema = "https"
        endpoint = f"{schema}://{user}:{api_key}@{host}:{port}/wallet"
        self.request = Request(endpoint, timeout)

    def create_wallet(
        self,
        wallet_id: str,
        type_: str = "pubkeyhash",
        master: Optional[str] = None,
        mnemonic: Optional[str] = None,
        passphrase: Optional[str] = None,
        witness: bool = False,
        m: int = 1,
        n: int = 1,
        watch_only: bool = False,
        account_key: Optional[str] = None,
        account_depth: int = 0,
    ) -> Dict[str, Any]:
        """
        Create a new wallet with a specified ID.
        see https://hsd-dev.org/api-docs/index.html?shell--curl#wallet
        """
        assert type(wallet_id) == str
        assert type(type_) == str
        assert master is None or type(master) == str
        assert mnemonic is None or type(mnemonic) == str
        assert passphrase is None or type(passphrase) == str
        assert type(witness) == bool
        assert type(m) == int
        assert type(n) == int
        assert type(watch_only) == bool
        assert account_key is None or type(account_key) == str
        assert type(account_depth) == int
        # default params
        params: Dict[str, Any] = {
            "witness": witness,
            "type": type_,
            "m": m,
            "n": n,
            "watchOnly": watch_only,
            "accountDepth": account_depth,
        }
        # Optional
        if master:
            params["master"] = master
        if mnemonic:
            params["mnemonic"] = mnemonic
        if passphrase:
            params["passphrase"] = passphrase
        if account_key:
            params["accountKey"] = account_key
        r = self.request.put(wallet_id, params=params)
        result = cast(Dict[str, Any], r)
        return result
