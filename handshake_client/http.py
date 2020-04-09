import json
from requests import get, post, put, delete
from requests.exceptions import ConnectionError, HTTPError
from typing import cast, Optional, Union, List, Dict, Any
from handshake_client.constant import TIMEOUT


class Request:
    def __init__(self, endpoint: str, timeout: int = TIMEOUT):
        assert type(endpoint) == str
        assert type(timeout) == int
        self.endpoint = endpoint
        self.timeout = timeout

    def get(self, path: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert type(path) == str
        return self.try_request("GET", path)

    def post(
        self, path: str, params: Dict[str, Any]
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert type(path) == str
        assert type(params) == dict
        return self.try_request("POST", path, params)

    def put(
        self, path: str, params: Dict[str, Any]
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert type(path) == str
        assert type(params) == dict
        return self.try_request("PUT", path, params)

    def delete(
        self, path: str, params: Dict[str, Any]
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert type(path) == str
        assert type(params) == dict
        return self.try_request("DELETE", path, params)

    def try_request(
        self, method: str, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        assert type(method) == str
        assert method in ["GET", "POST", "PUT", "DELETE"]
        assert type(path) == str
        assert params is None or type(params) == dict
        try:
            headers = {"Content-Type": "application/json"}
            if method == "GET":
                r = get(self.endpoint + "/" + path, timeout=self.timeout)
            elif method == "POST":
                r = post(
                    self.endpoint + "/" + path,
                    data=json.dumps(params),
                    headers=headers,
                    timeout=self.timeout,
                )
            elif method == "PUT":
                r = put(
                    self.endpoint + "/" + path,
                    data=json.dumps(params),
                    timeout=self.timeout,
                )
            elif method == "DELETE":
                r = delete(
                    self.endpoint + "/" + path,
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
        wallet_id: str,
        api_key: str,
        host: str,
        port: str,
        user: str = "x",
        ssl: bool = False,
        timeout: int = TIMEOUT,
    ):
        assert type(wallet_id) == str
        assert type(api_key) == str
        assert type(host) == str
        assert type(port) == str
        assert type(user) == str
        assert type(ssl) == bool
        assert type(timeout) == int
        schema: str = "http"
        if ssl is True:
            schema = "https"
        endpoint = f"{schema}://{user}:{api_key}@{host}:{port}/wallet/{wallet_id}/"
        self.request = Request(endpoint, timeout)

    def create_wallet(
        self,
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
        r = self.request.put("", params=params)
        result = cast(Dict[str, Any], r)
        return result

    def reset_token(self, passphrase: Optional[str] = None) -> Dict[str, str]:
        assert passphrase is None or type(passphrase) == str
        params: Dict[str, str] = {}
        if passphrase:
            params["passphrase"] = passphrase
        r = self.request.post(f"retoken", params=params)
        result = cast(Dict[str, str], r)
        return result

    def get_wallet_info(self) -> Dict[str, Any]:
        r = self.request.get("")
        result = cast(Dict[str, Any], r)
        return result

    def get_master_hd_key(self) -> Dict[str, Any]:
        r = self.request.get("master")
        result = cast(Dict[str, Any], r)
        return result

    def change_passphrase(self, old_pass: str, new_pass: str) -> Dict[str, bool]:
        assert type(old_pass) == str
        assert type(new_pass) == str
        params = {"old": old_pass, "passphrase": new_pass}
        r = self.request.post("passphrase", params)
        result = cast(Dict[str, bool], r)
        return result

    def send_transaction(
        self,
        outputs: List[Dict[str, Any]],
        passphrase: Optional[str] = None,
        rate: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create, sign, and send a transaction.
        outputs ex:
            [{"address":"'$address'", "value":'$value'}
        """
        assert type(outputs) == list
        assert passphrase is None or type(passphrase) == str
        assert rate is None or type(rate) == int
        params = {"outputs": outputs, "passphrase": passphrase, "rate": rate}
        # TODO params多すぎるので一旦updateで対応してる
        params.update(kwargs)
        r = self.request.post("send", params)
        result = cast(Dict[str, Any], r)
        return result

    def create_transaction(
        self,
        outputs: List[Dict[str, Any]],
        passphrase: Optional[str] = None,
        rate: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create and template a transaction (useful for multisig)
        outputs ex:
            [{"address":"'$address'", "value":'$value'}
        """
        assert type(outputs) == list
        assert passphrase is None or type(passphrase) == str
        assert rate is None or type(rate) == int
        params = {"outputs": outputs, "passphrase": passphrase, "rate": rate}
        # TODO params多すぎるので一旦updateで対応してる
        params.update(kwargs)
        r = self.request.post("create", params)
        result = cast(Dict[str, Any], r)
        return result

    def sign_transaction(
        self, tx_hex: str, passphrase: Optional[str] = None
    ) -> Dict[str, Any]:
        assert type(tx_hex) == str
        assert passphrase is None or type(passphrase) == str
        params = {"tx": tx_hex, "passphrase": passphrase}
        r = self.request.post("sign", params)
        result = cast(Dict[str, Any], r)
        return result

    def zap_transactions(self, account: str, age: int) -> Dict[str, bool]:
        """
        Remove all pending transactions older than a specified age.
        """
        assert type(account) == str
        assert type(age) == int
        params = {"account": account, "age": age}
        # TODO correct path?
        r = self.request.post("zap?age=3600", params)
        result = cast(Dict[str, bool], r)
        return result

    def unlock_wallet(
        self, passphrase: Optional[str] = None, timeout: int = 60
    ) -> Dict[str, bool]:
        assert passphrase is None or type(passphrase) == str
        assert type(timeout) == int
        params = {"passphrase": passphrase, "timeout": timeout}
        r = self.request.post("unlock", params)
        result = cast(Dict[str, bool], r)
        return result

    def lock_wallet(self) -> Dict[str, bool]:
        r = self.request.post("lock", {})
        result = cast(Dict[str, bool], r)
        return result

    def import_privkey(self, account: str, privkey: str) -> Dict[str, bool]:
        assert type(account) == str
        assert type(privkey) == str
        params = {"account": account, "privateKey": privkey}
        r = self.request.post("import", params)
        result = cast(Dict[str, bool], r)
        return result

    def import_pubkey(self, account: str, pubkey: str) -> Dict[str, bool]:
        assert type(account) == str
        assert type(pubkey) == str
        # import watch-only
        params = {"account": account, "publicKey": pubkey}
        r = self.request.post("import", params)
        result = cast(Dict[str, bool], r)
        return result

    def import_address(self, account: str, address: str) -> Dict[str, bool]:
        assert type(account) == str
        assert type(address) == str
        # import watch-only
        params = {"account": account, "address": address}
        r = self.request.post("import", params)
        result = cast(Dict[str, bool], r)
        return result

    def get_blocks_with_txs(self) -> List[str]:
        """
        List all block heights which contain any wallet transactions.
        Returns an array of block heights
        """
        r = self.request.get("block")
        result = cast(List[str], r)
        return result

    def get_wallet_by_block_height(self, block_height: int) -> Dict[str, Any]:
        assert type(block_height) == int
        r = self.request.get(f"block/{block_height}")
        result = cast(Dict[str, Any], r)
        return result

    def add_shared_key(self, account: str, xpubkey: str) -> Dict[str, bool]:
        assert type(account) == str
        assert type(xpubkey) == str
        params = {"accountKey": xpubkey, "account": account}
        r = self.request.put("shared-key", params)
        result = cast(Dict[str, bool], r)
        return result
