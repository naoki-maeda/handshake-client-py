from typing import List, Dict, Any
from bitcoinrpc.authproxy import AuthServiceProxy


class RpcClient:
    def __init__(self, api_key: str, host: str, port: str):
        assert type(api_key) == str
        assert type(host) == str
        assert type(port) == str
        self.proxy = AuthServiceProxy(f"http://x:{api_key}@{host}:{port}")

    def getinfo(self) -> Dict[str, Any]:
        return self.proxy.getinfo()

    def getmemoryinfo(self) -> Dict[str, Any]:
        return self.proxy.getmemoryinfo()

    def setloglevel(self, level: str) -> None:
        assert type(level) == str
        self.proxy.setloglevel(level)

    def validateaddress(self, address: str) -> Dict[str, Any]:
        assert type(address) == str
        return self.proxy.validateaddress(address)

    def createmultisig(self, n_required: int, pubkeys: List[str]) -> Dict[str, Any]:
        """
        n_required: Required number of approvals for spending
        pubkeys: List of public keys
        """
        assert type(n_required) == int
        assert type(pubkeys) == list
        return self.proxy.createmultisig(n_required, pubkeys)

    def signmessagewithprivkey(self, privkey: str, message: str) -> Dict[str, Any]:
        """
        privkey: Private key
        message: Message you want to sign.
        """
        assert type(privkey) == str
        assert type(message) == str
        return self.proxy.signmessagewithprivkey(privkey, message)

    def verifymessage(self, address: str, signature: str, message: str) -> Dict[str, Any]:
        """
        address: Address of the signer
        signature: Signature of signed message
        message: Message that was signed
        """
        assert type(address) == str
        assert type(signature) == str
        assert type(message) == str
        return self.proxy.verifymessage(address, signature, message)

    def setmocktime(self, timestamp: int) -> None:
        """
        Changes network time (This is consensus-critical)
        timestamp: unixtime
        """
        assert type(timestamp) == int
        self.proxy.setmocktime(timestamp)
